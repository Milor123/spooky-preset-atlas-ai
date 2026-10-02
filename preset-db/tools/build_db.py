"""Build the Spooky2 preset SQLite database from the read-only txt corpus.

Usage
    python build_db.py --pilot          # ~1,500-file stratified sample
    python build_db.py --full           # every file in the corpus
    python build_db.py --pilot --json   # machine-readable audit

Invariants
----------
* The corpus is opened read-only. This script writes only under preset-db/.
* Every filename is stored whole. Mode tokens such as ``(R)``, ``(C)``, ``(Coil)``
  are kept literally AND surfaced as shell/mode columns; they are never stripped
  to make the name tidier.
* Every frequency keeps its raw token. The tilde and backtick notations are
  proprietary program data and are recorded, not decoded.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sqlite3
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spooky import extract as ex  # noqa: E402
from spooky.parser import (  # noqa: E402
    DB_GLOSSARY,
    database_tag,
    iter_corpus_files,
    read_and_parse,
    token_shape,
    tokenize_frequencies,
)

HERE = os.path.dirname(os.path.abspath(__file__))   # .../preset-db/tools
DB_ROOT = os.path.dirname(HERE)                      # .../preset-db

# Corpus discovery, in priority order:
#   1. explicit --corpus
#   2. SPOOKY2_CORPUS environment variable
#   3. a real Spooky2 install (S: first, because that is where this user keeps
#      it, then the usual Program Files location)
#   4. a working copy sitting next to this repo
# Never hardcode one machine's path: the whole point of the rebuilder is that it
# still works after a Windows reinstall, an upgrade, or on a different drive.
CANDIDATE_CORPUS = [
    r"S:\Spooky2\Preset Collections",
    r"C:\Program Files\Spooky2\Preset Collections",
    r"C:\Program Files (x86)\Spooky2\Preset Collections",
    os.path.join(os.path.dirname(DB_ROOT), "Preset Collections"),
]

# Folders never indexed. The guide is explicit that a user's own presets live in
# Preset Collections/User, and mixing them into the factory index would make the
# question "what does Spooky2 actually ship" unanswerable. Opt back in with
# --include-user.
EXCLUDED_DIRS = ("user",)


def find_corpus(explicit: str | None = None) -> str:
    candidates: list[str] = []
    if explicit:
        candidates.append(explicit)
    env = os.environ.get("SPOOKY2_CORPUS")
    if env:
        candidates.append(env)
    candidates.extend(CANDIDATE_CORPUS)
    for path in candidates:
        if path and os.path.isdir(path):
            return path
    raise SystemExit(
        "could not find the Spooky2 'Preset Collections' folder.\ntried:\n  "
        + "\n  ".join(c for c in candidates if c)
        + "\nfix it by setting SPOOKY2_CORPUS or passing --corpus")


SCHEMA = os.path.join(DB_ROOT, "schema", "schema.sql")

PRESET_COLUMNS = [
    "id", "source_file_id", "ordinal",
    "filename_full", "filename_stem", "filename_slug", "preset_name", "base_preset",
    "author_id", "collection_id", "shell_id", "mode_id",
    "l1", "l2", "l3", "l4",
    "description", "notes_full", "notes_lead", "notes_len", "has_description",
    "program_count", "freq_count",
    "schedule_run_for", "schedule_run_from", "schedule_run_to",
    "repeat_sequence", "repeat_chain", "dedupe_enabled", "dedupe_tolerance",
    "params_json", "flags_json",
]


def _scalar(value):
    """Promoted hot columns must be scalar. A key repeated inside one preset
    yields a list; the first value wins and the full list stays in params_json."""
    if isinstance(value, list):
        return value[0] if value else None
    return value


# staging bookkeeping, keyed by id(connection). sqlite3.Connection does not
# accept arbitrary attributes, so this cannot live on the connection object.
_STAGING: dict[int, tuple[str, str]] = {}


def connect(db_path: str) -> sqlite3.Connection:
    """Open a NEW database beside the target and swap it in only on success.

    An earlier version deleted the target first, so a build interrupted part-way
    through (Ctrl-C, a crash, a killed process) left a zero-byte database where a
    perfectly good one had been. Build under a .building name and rename at the
    end, so a failed build can never destroy the previous one.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    staging = db_path + ".building"
    for path in (staging, staging + "-wal", staging + "-shm"):
        if os.path.exists(path):
            os.remove(path)
    con = sqlite3.connect(staging)
    con.executescript(open(SCHEMA, encoding="utf-8").read())
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=OFF")
    con.execute("PRAGMA cache_size=-131072")

    _STAGING[id(con)] = (staging, db_path)
    return con


def finalize(con: sqlite3.Connection) -> None:
    """Close cleanly and move the freshly built database over the target."""
    entry = _STAGING.pop(id(con), None)
    con.commit()
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    con.close()
    if not entry:
        return
    staging, target = entry
    if os.path.exists(target):
        os.remove(target)
    os.replace(staging, target)
    for suffix in ("-wal", "-shm"):
        if os.path.exists(staging + suffix):
            os.remove(staging + suffix)


def stratified_sample(all_files: list[tuple[str, str]], n: int, seed: int = 7):
    """Proportional sample across top-level collections, minimum 15 files each."""
    by_collection: dict[str, list] = defaultdict(list)
    for item in all_files:
        by_collection[item[1].split("/")[0]].append(item)
    rng = random.Random(seed)
    total = len(all_files)
    out: list[tuple[str, str]] = []
    for coll in sorted(by_collection):
        pool = sorted(by_collection[coll])
        take = max(15, round(len(pool) * n / total))
        out.extend(rng.sample(pool, min(take, len(pool))))
    return sorted(out)


def build(sample_size: int | None, db_path: str, report_only: bool = False,
          corpus: str | None = None, include_user: bool = False) -> dict:
    t0 = time.time()
    corpus_root = find_corpus(corpus)
    print(f"corpus: {corpus_root}")
    if not os.path.isdir(corpus_root):
        raise SystemExit(f"corpus not found: {corpus_root}")

    all_files = sorted(iter_corpus_files(corpus_root, (".txt",)))
    if not include_user:
        before = len(all_files)
        all_files = [f for f in all_files
                     if not any(seg.lower() in EXCLUDED_DIRS
                                for seg in f[1].split("/")[:-1])]
        if len(all_files) != before:
            print(f"excluded {before - len(all_files)} personal files under "
                  f"{'/'.join(EXCLUDED_DIRS)}/ (--include-user to index them)")
    files = all_files if sample_size is None else stratified_sample(all_files, sample_size)
    print(f"files: {len(files):,} of {len(all_files):,} indexable")

    con = sqlite3.connect(":memory:") if report_only else connect(db_path)

    stats: Counter = Counter()
    unknown_shapes: Counter = Counter()
    shape_example: dict[str, str] = {}
    shape_notation: dict[str, str] = {}
    issues: list[tuple] = []
    other_sections: Counter = Counter()
    key_freq: Counter = Counter()
    per_collection: Counter = Counter()
    per_author: Counter = Counter()
    per_shell: Counter = Counter()
    per_mode: Counter = Counter()

    src_rows: list[dict] = []
    preset_rows: list[dict] = []
    program_rows: list[dict] = []
    freq_rows: list[dict] = []
    tag_defs: dict[str, tuple] = {}
    tag_rows: list[tuple] = []
    dur_rows: list[tuple] = []
    warn_rows: list[tuple] = []
    name_fts_rows: list[tuple] = []
    doc_fts_rows: list[tuple] = []

    next_preset_id = 1
    next_program_id = 1

    for file_index, (abs_path, rel_path) in enumerate(files):
        pf = read_and_parse(abs_path, rel_path)
        segments = rel_path.split("/")
        collection = segments[0]
        folders = segments[1:-1]
        filename = segments[-1]
        stem = os.path.splitext(filename)[0]

        src_rows.append({
            "path": rel_path, "filename": filename, "stem": stem,
            "dir_path": "/".join(folders), "byte_size": pf.byte_size,
            "content_hash": pf.content_hash, "preset_count": len(pf.presets),
            "section_count": len(pf.other_sections),
        })
        for sec in pf.other_sections:
            other_sections[sec] += 1
        issues.extend((i.path, i.line_no, i.kind, i.detail, i.excerpt) for i in pf.issues)
        stats["files"] += 1

        for preset in pf.presets:
            preset_id = next_preset_id
            next_preset_id += 1
            stats["presets"] += 1
            per_collection[collection] += 1

            preset_name = preset.first("PresetName") or ""
            base_preset = preset.first("Base_Preset")
            notes = preset.first("Preset_Notes") or ""
            lead = ex.notes_lead(notes)
            description = lead or stem
            has_description = 1 if lead else 0

            author = ex.derive_author(stem)
            modes = ex.derive_modes(stem)
            mode = modes[-1] if modes else None
            shell = ex.derive_shell(base_preset, folders, modes)
            if author:
                per_author[author] += 1
            if shell:
                per_shell[shell] += 1
            if mode:
                per_mode[mode] += 1

            params: dict[str, object] = {}
            for key, values in preset.keys.items():
                key_freq[key] += 1
                if key in ("Preset_Notes", "Loaded_Programs", "Loaded_Frequencies"):
                    continue
                params[key] = values if len(values) > 1 else values[0]

            flags = {
                "is_biofeedback": any(k.startswith("BFB_") for k in preset.keys)
                or "BiofeedbackPreset" in preset.keys,
                "is_sweep": "sweep" in rel_path.lower(),
                "is_chain": "Repeat_Chain" in preset.keys or len(pf.presets) > 1,
                "is_dna": "(DNA)" in stem or "/DNA/" in f"/{rel_path}",
                "is_peptide": "peptide" in rel_path.lower(),
                "has_notes": bool(notes),
                "has_description": bool(lead),
                "modes": modes,
            }

            prog_names = preset.all("Loaded_Programs")
            freq_lines = preset.all("Loaded_Frequencies")

            preset_rows.append({
                "id": preset_id, "source_file_id": file_index + 1, "ordinal": preset.ordinal,
                "filename_full": filename, "filename_stem": stem,
                "filename_slug": stem.casefold(),
                "preset_name": preset_name, "base_preset": base_preset,
                "author_id": author, "collection_id": collection, "shell_id": shell,
                "mode_id": mode,
                "l1": folders[0] if len(folders) > 0 else None,
                "l2": folders[1] if len(folders) > 1 else None,
                "l3": folders[2] if len(folders) > 2 else None,
                "l4": folders[3] if len(folders) > 3 else None,
                "description": description, "notes_full": notes, "notes_lead": lead,
                "notes_len": len(notes), "has_description": has_description,
                "program_count": len(prog_names), "freq_count": 0,
                "schedule_run_for": _scalar(params.get("Schedule_Run_For")),
                "schedule_run_from": _scalar(params.get("Schedule_Run_From")),
                "schedule_run_to": _scalar(params.get("Schedule_Run_To")),
                "repeat_sequence": _scalar(params.get("Repeat_Sequence")),
                "repeat_chain": _scalar(params.get("Repeat_Chain")),
                "dedupe_enabled": _scalar(params.get("Enable_Remove_Duplicate_Frequencies")),
                "dedupe_tolerance": _scalar(params.get("Remove_Duplicate_Frequencies_Tolerance")),
                "params_json": json.dumps(params, ensure_ascii=False),
                "flags_json": json.dumps(flags, ensure_ascii=False),
            })
            name_fts_rows.append((stem, stem.casefold(), preset_name))
            stats["notes_bytes"] += len(notes)
            if has_description:
                stats["descriptions"] += 1

            # Tags read intent, so they are matched against the name, the folder
            # and the opening lines only. Matching the full notes produced 73-98%
            # false positives: any organism name can appear incidentally in 4 KB of
            # prose. Durations and warnings are different - they legitimately sit
            # deep in the notes - so those still get the full text.
            tag_haystack = "\n".join([preset_name, stem, lead])
            for h in ex.extract_tags(tag_haystack, folders, stem, preset_name):
                tag_defs.setdefault(h.slug, (h.slug, h.label, h.category))
                tag_rows.append((preset_id, h.slug, h.source, h.confidence, h.evidence))

            for d in ex.extract_durations(notes):
                dur_rows.append((preset_id, d.kind, d.value_text, d.minutes, d.evidence))
            for w in ex.extract_warnings(notes, preset_name):
                warn_rows.append((preset_id, w.kind, w.evidence))

            stats["programs"] += len(prog_names)
            stats["freq_lines"] += len(freq_lines)

            for ordinal in range(max(len(prog_names), len(freq_lines))):
                program_id = next_program_id
                next_program_id += 1
                pname = prog_names[ordinal] if ordinal < len(prog_names) else None
                fraw = freq_lines[ordinal] if ordinal < len(freq_lines) else None
                program_rows.append({
                    "id": program_id, "preset_id": preset_id, "ordinal": ordinal,
                    "program_name": pname, "freq_line_raw": fraw,
                    "database_tag": database_tag(pname),
                })
                if not fraw:
                    stats["programs_without_freq"] += 1
                    continue
                for tok in tokenize_frequencies(fraw):
                    freq_rows.append({
                        "id": len(freq_rows) + 1, "program_id": program_id, "ordinal": tok.ordinal,
                        "notation": tok.notation, "raw_token": tok.raw,
                        "hz_lo": tok.hz_lo, "hz_hi": tok.hz_hi, "amplitude": tok.amplitude,
                        "modifiers": tok.modifiers, "codes": tok.codes,
                        "nums_json": json.dumps(tok.nums), "parse_status": tok.parse_status,
                    })
                    stats["frequencies"] += 1
                    stats[f"notation_{tok.notation}"] += 1
                    stats[f"status_{tok.parse_status}"] += 1
                    if tok.parse_status == "unparsed":
                        sh = token_shape(tok.raw)
                        unknown_shapes[sh] += 1
                        shape_example.setdefault(sh, tok.raw)
                        shape_notation.setdefault(sh, tok.notation)

        if file_index % 1000 == 999:
            print(f"  parsed {file_index + 1}/{len(files)} files", flush=True)

    if not report_only:
        _write(con, src_rows, preset_rows, program_rows, freq_rows, tag_defs,
               tag_rows, dur_rows, warn_rows, name_fts_rows, doc_fts_rows,
               unknown_shapes, shape_example, shape_notation, issues, stats)

    return {
        "elapsed_s": round(time.time() - t0, 1),
        "stats": dict(stats),
        "collections": per_collection.most_common(),
        "authors": per_author.most_common(),
        "shells": per_shell.most_common(),
        "modes": per_mode.most_common(),
        "distinct_keys": len(key_freq),
        "top_keys": key_freq.most_common(15),
        "parse_issues": Counter(k for _, _, k, _, _ in issues).most_common(),
        "unknown_shapes": unknown_shapes.most_common(15),
        "other_sections": other_sections.most_common(),
        "missing_description": stats["presets"] - stats.get("descriptions", 0),
    }


def _write(con, src_rows, preset_rows, program_rows, freq_rows, tag_defs,
           tag_rows, dur_rows, warn_rows, name_fts_rows, doc_fts_rows,
           unknown_shapes, shape_example, shape_notation, issues, stats) -> None:
    con.executemany("INSERT INTO collection (name) VALUES (?)",
                    [(c,) for c in sorted({r["collection_id"] for r in preset_rows
                                           if r["collection_id"]})])
    for code, name in ex.KNOWN_AUTHORS.items():
        con.execute("INSERT OR IGNORE INTO author (code, confirmed_name) VALUES (?,?)",
                    (code, name))
    con.executemany("INSERT OR IGNORE INTO shell (name, description) VALUES (?,?)",
                    [(k, v) for k, v in ex.SHELLS.items()])
    # The guide's p64 pane lists 16 tickable databases and omits RRM; Spooky2's own
    # glossary has 17. Record the difference rather than silently normalising it.
    guide_16 = {"ALT", "BFB", "BIO", "CAFL", "CUST", "DNA", "ETDFL", "HC", "KHZ",
                "MW", "PROV", "RIFE", "RUSS", "SD", "VEGA", "XTRA"}
    con.executemany("INSERT OR IGNORE INTO database (code, description, in_guide_16)"
                    " VALUES (?,?,?)",
                    [(code, desc, 1 if code in guide_16 else 0)
                     for code, desc in DB_GLOSSARY.items()])
    con.executemany("INSERT OR IGNORE INTO mode (token, label) VALUES (?,?)",
                    [(k, v) for k, v in ex.MODES.items()])

    con.executemany(
        "INSERT INTO source_file (id, path, filename, stem, dir_path, byte_size,"
        " content_hash, preset_count, section_count)"
        " VALUES (:id,:path,:filename,:stem,:dir_path,:byte_size,:content_hash,"
        ":preset_count,:section_count)",
        [dict(r, id=i + 1) for i, r in enumerate(src_rows)],
    )

    author_ids = {r[0]: r[1] for r in con.execute("SELECT code, id FROM author")}
    coll_ids = {r[0]: r[1] for r in con.execute("SELECT name, id FROM collection")}
    shell_ids = {r[0]: r[1] for r in con.execute("SELECT name, id FROM shell")}
    mode_ids = {r[0]: r[1] for r in con.execute("SELECT token, id FROM mode")}

    for r in preset_rows:
        r["author_id"] = author_ids.get(r["author_id"])
        r["collection_id"] = coll_ids.get(r["collection_id"])
        r["shell_id"] = shell_ids.get(r["shell_id"])
        r["mode_id"] = mode_ids.get(r["mode_id"])

    con.executemany(
        f"INSERT INTO preset ({','.join(PRESET_COLUMNS)})"
        f" VALUES ({','.join(':' + c for c in PRESET_COLUMNS)})", preset_rows)
    con.executemany(
        "INSERT INTO program (id, preset_id, ordinal, program_name, database_tag,"
        " freq_line_raw) VALUES (:id,:preset_id,:ordinal,:program_name,:database_tag,"
        ":freq_line_raw)", program_rows)
    con.executemany("INSERT INTO programs_fts (rowid, program_name) VALUES (?,?)",
                    [(r["id"], r["program_name"]) for r in program_rows
                     if r["program_name"]])
    con.executemany(
        "INSERT INTO frequency (id, program_id, ordinal, notation, raw_token, hz_lo, hz_hi,"
        " amplitude, modifiers, codes, nums_json, parse_status)"
        " VALUES (:id,:program_id,:ordinal,:notation,:raw_token,:hz_lo,:hz_hi,"
        ":amplitude,:modifiers,:codes,:nums_json,:parse_status)", freq_rows)
    con.commit()

    con.execute(
        "UPDATE preset SET freq_count = (SELECT COUNT(*) FROM frequency f"
        " JOIN program pr ON pr.id = f.program_id WHERE pr.preset_id = preset.id)")
    con.commit()

    con.executemany("INSERT OR IGNORE INTO tag (slug, label, category) VALUES (?,?,?)",
                    list(tag_defs.values()))
    tag_ids = {r[0]: r[1] for r in con.execute("SELECT slug, id FROM tag")}
    con.executemany(
        "INSERT OR IGNORE INTO preset_tag (preset_id, tag_id, source, confidence, evidence)"
        " VALUES (?,?,?,?,?)",
        [(p, tag_ids[s], src, conf, ev) for p, s, src, conf, ev in tag_rows if s in tag_ids])
    con.executemany(
        "INSERT INTO preset_duration (preset_id, kind, value_text, minutes, evidence)"
        " VALUES (?,?,?,?,?)", dur_rows)
    con.executemany("INSERT INTO preset_warning (preset_id, kind, evidence) VALUES (?,?,?)",
                    warn_rows)
    con.executemany("INSERT INTO name_fts VALUES (?,?,?)", name_fts_rows)
    con.executemany("INSERT INTO preset_fts (filename_stem, preset_name, notes_lead, notes_full)"
                    " VALUES (?,?,?,?)",
                    [(r["filename_stem"], r["preset_name"], r["notes_lead"], r["notes_full"])
                     for r in preset_rows])

    con.executemany("INSERT INTO unknown_shape (notation, shape, hits, example)"
                    " VALUES (?,?,?,?)",
                    [(shape_notation[s], s, c, shape_example[s])
                     for s, c in unknown_shapes.most_common()])
    con.executemany("INSERT INTO parse_issue (path, line_no, kind, detail, excerpt)"
                    " VALUES (?,?,?,?,?)", issues)
    con.executemany("INSERT OR REPLACE INTO build_stat (label, value) VALUES (?,?)",
                    [(k, str(v)) for k, v in stats.items()])
    con.commit()
    con.execute("ANALYZE")
    con.commit()
    # Roll the database-origin counts up from the programs actually present, so the
    # glossary can show what this corpus really contains rather than only the
    # official description.
    con.execute("""
        UPDATE database SET
          program_count = (SELECT COUNT(*) FROM program pr
                            WHERE pr.database_tag = database.code),
          preset_count  = (SELECT COUNT(DISTINCT pr.preset_id) FROM program pr
                            WHERE pr.database_tag = database.code)
    """)
    con.commit()
    finalize(con)


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pilot", type=int, nargs="?", const=1500,
                   help="stratified sample size (default 1500)")
    g.add_argument("--full", action="store_true", help="every corpus file")
    ap.add_argument("--db", default=os.path.join(DB_ROOT, "build", "spooky.db"))
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--corpus", help="path to Preset Collections (default: auto-detect)")
    ap.add_argument("--include-user", action="store_true",
                    help="also index Preset Collections/User (your own presets)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    sample = None if args.full else args.pilot
    report = build(sample, args.db, report_only=args.report_only,
                   corpus=args.corpus, include_user=args.include_user)

    if args.json:
        print(json.dumps(report, indent=2, default=str))
        return 0

    s = report["stats"]
    print()
    print("=" * 68)
    print(f"  elapsed                {report['elapsed_s']}s")
    print(f"  files                  {s.get('files', 0):,}")
    print(f"  presets                {s.get('presets', 0):,}")
    print(f"  with description       {s.get('descriptions', 0):,}")
    print(f"  without description    {report['missing_description']:,}")
    print(f"  programs               {s.get('programs', 0):,}")
    print(f"  frequencies            {s.get('frequencies', 0):,}")
    print(f"  notes prose            {s.get('notes_bytes', 0) / 1e6:.1f} MB")
    print(f"  programs without freq  {s.get('programs_without_freq', 0):,}")
    print("  " + "-" * 64)
    for k in sorted(k for k in s if k.startswith(("notation_", "status_"))):
        print(f"  {k:<24} {s[k]:,}")
    print("  " + "-" * 64)
    print(f"  distinct keys          {report['distinct_keys']}")
    print(f"  authors                {report['authors'][:8]}")
    print(f"  shells                 {report['shells']}")
    print(f"  modes                  {report['modes']}")
    print(f"  parse issues           {report['parse_issues'] or 'none'}")
    print(f"  unknown shapes         {len(report['unknown_shapes'])}")
    for shape, count in report["unknown_shapes"][:10]:
        print(f"      {count:>6,}  {shape}")
    print("=" * 68)
    if not args.report_only:
        print(f"db: {args.db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())