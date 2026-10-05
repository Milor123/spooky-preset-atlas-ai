"""Query the Spooky2 preset database. This is the tool the skill calls.

Design rule: the default output never includes notes_full or frequency rows.
Those are only returned when explicitly asked for, because they are what makes
the raw txt corpus expensive.

Examples
    python query.py find "peptic ulcer"
    python query.py find "candida" --shell Remote --mode R --limit 8
    python query.py tags --organ lung
    python query.py get 42282              # catalog row + programs, no prose
    python query.py get 42282 --notes      # + full description (expensive)
    python query.py get 42282 --freqs      # + every frequency (expensive)
    python query.py freqs --hz 10000 --limit 20
    python query.py stats
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DB_ROOT = os.path.dirname(HERE)
DEFAULT_DB = os.path.join(DB_ROOT, "build", "spooky.db")

CATALOG_COLUMNS = """
    p.id, p.filename_full, p.preset_name, p.description,
    a.code AS author, c.name AS collection, sh.name AS shell, m.token AS mode,
    p.program_count, p.freq_count, p.notes_len, s.path AS path
"""


def connect(path: str) -> sqlite3.Connection:
    if not os.path.exists(path):
        raise SystemExit(f"database not found: {path}\nbuild it with: python build_db.py --full")
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    con.create_function("regexp", 2, _regexp)
    return con


def _regexp(pattern: str, value) -> bool:
    if value is None:
        return False
    try:
        return re.search(pattern, str(value), re.IGNORECASE) is not None
    except re.error as exc:
        raise SystemExit(f"invalid --regex pattern {pattern!r}: {exc}")


def fts_query(text: str) -> str:
    """Turn free text into a safe FTS5 MATCH expression."""
    terms = []
    for raw in text.split():
        cleaned = "".join(ch if ch.isalnum() else " " for ch in raw).split()
        terms.extend(cleaned)
    if not terms:
        raise SystemExit("no searchable terms in the query")
    return " OR ".join(f'"{t}"' for t in terms)


def program_matches(con, expr: str, limit: int = 300) -> dict[int, list[str]]:
    """preset_id -> the program names that matched.

    This is the deep search. A preset's title rarely names what it treats while
    its program list does: "Leaky Gut Healing Therapy (CL) - JD" loads
    "Ropeworm (XTRA)" and "Biofilms 01 (XTRA)", so a search for "ropeworm" must
    reach it even though the word appears in neither the filename nor the notes.

    Returning WHICH program matched is the whole point. A hit with no evidence is
    noise; a hit that says "matched: Ropeworm (XTRA)" is the most useful signal in
    the system, because the title understates and the program list does not.
    """
    rows = con.execute("""
        SELECT pr.preset_id AS pid, pr.program_name AS pname
          FROM programs_fts JOIN program pr ON pr.id = programs_fts.rowid
         WHERE programs_fts MATCH ?
         LIMIT ?
    """, (expr, limit * 20)).fetchall()
    out: dict[int, list[str]] = {}
    for pid, pname in rows:
        bucket = out.setdefault(pid, [])
        if pname not in bucket:
            bucket.append(pname)
    return out


def cmd_dbinfo(con, args) -> int:
    """Spooky2's official database glossary, with what this corpus actually holds."""
    rows = con.execute("""
        SELECT code, description, program_count, preset_count, in_guide_16
          FROM database ORDER BY program_count DESC, code
    """).fetchall()
    if args.json:
        print(json.dumps([dict(r) for r in rows], indent=2, ensure_ascii=False))
        return 0
    print(f"Spooky2 database glossary -- {len(rows)} codes. "
          f"progs = programs in this corpus, presets = presets using them.\n")
    print(f"  {'code':<6}{'progs':>8}{'presets':>9}  description")
    for r in rows:
        flag = "" if r["in_guide_16"] else "  (not in the guide's list of 16)"
        print(f"  {r['code']:<6}{r['program_count']:>8,}{r['preset_count']:>9,}  "
              f"{r['description']}{flag}")
    total = sum(r["program_count"] for r in rows)
    print(f"\n  {total:,} of {con.execute('SELECT COUNT(*) FROM program').fetchone()[0]:,}"
          f" programs carry a database tag; the rest are untagged custom programs.")
    return 0


def cmd_find(con, args) -> int:
    # Three search modes, because the corpus names things in two different places.
    #
    #   names  - name_fts only: filename_stem, filename_slug, preset_name.
    #   all    - preset_fts: the same three PLUS notes_lead and notes_full, with
    #            bm25 column weights so a name match always outranks a prose
    #            match. This is the default, because authors routinely name the
    #            exact organism ONLY in the prose: "Threadworms (C)" describes
    #            itself as "pinworms (Enterobius vermicularis)", so a name-only
    #            search for "enterobius" never finds it.
    #   notes  - preset_fts restricted to prose matches.
    #
    # The earlier --in notes was a WHERE name_fts MATCH ? AND <notes condition>,
    # which is an AND: it could only ever narrow, never widen. Hence it silently
    # returned identical results to the name-only search.
    #
    # name_fts is joined on rowid, NOT on filename_stem: that column is not unique
    # (chain files hold up to 222 presets sharing one stem) and a name join
    # produced a cartesian blow-up.
    expr = fts_query(args.query)
    if args.regex:
        sql = f"""
            SELECT {CATALOG_COLUMNS},
                   (SELECT group_concat(DISTINCT t.label) FROM preset_tag pt
                      JOIN tag t ON t.id = pt.tag_id WHERE pt.preset_id = p.id) AS tags
              FROM preset p
              JOIN source_file s ON s.id = p.source_file_id
              LEFT JOIN author a     ON a.id = p.author_id
              LEFT JOIN collection c ON c.id = p.collection_id
              LEFT JOIN shell sh     ON sh.id = p.shell_id
              LEFT JOIN mode m       ON m.id = p.mode_id
             WHERE (p.filename_stem REGEXP ? OR p.preset_name REGEXP ?)
        """
        params: list = [args.query, args.query]
    elif args.in_ == "names":
        sql = f"""
            SELECT {CATALOG_COLUMNS}, bm25(name_fts) AS score,
                   (SELECT group_concat(DISTINCT t.label) FROM preset_tag pt
                      JOIN tag t ON t.id = pt.tag_id WHERE pt.preset_id = p.id) AS tags
              FROM name_fts
              JOIN preset p      ON p.id = name_fts.rowid
              JOIN source_file s ON s.id = p.source_file_id
              LEFT JOIN author a     ON a.id = p.author_id
              LEFT JOIN collection c ON c.id = p.collection_id
              LEFT JOIN shell sh     ON sh.id = p.shell_id
              LEFT JOIN mode m       ON m.id = p.mode_id
             WHERE name_fts MATCH ?
        """
        params = [expr]
    elif args.in_ == "programs":
        # Deep search: drive from the program index, then show which program hit.
        matches = program_matches(con, expr, limit=args.limit * 10)
        if not matches:
            print("no program in the corpus matches that")
            return 1
        pids = list(matches)[: args.limit]
        ph = ",".join("?" * len(pids))
        sql = f"""
            SELECT {CATALOG_COLUMNS}, 0 AS score,
                   (SELECT group_concat(DISTINCT t.label) FROM preset_tag pt
                      JOIN tag t ON t.id=pt.tag_id WHERE pt.preset_id=p.id) AS tags
              FROM preset p JOIN source_file s ON s.id=p.source_file_id
              LEFT JOIN author a     ON a.id=p.author_id
              LEFT JOIN collection c ON c.id=p.collection_id
              LEFT JOIN shell sh     ON sh.id=p.shell_id
              LEFT JOIN mode m       ON m.id=p.mode_id
             WHERE p.id IN ({ph})
        """
        params = [int(x) for x in pids]
        for col, val in (("sh.name", args.shell), ("m.token", args.mode),
                         ("a.code", args.author), ("c.name", args.collection)):
            if val:
                sql += f" AND {col} = ?"
                params.append(val)
        rows = con.execute(sql, params).fetchall()
        out_rows = []
        for r in rows:
            d = dict(r)
            d["matched_programs"] = ", ".join(matches.get(d["id"], [])[:4])
            out_rows.append(d)
        return emit(out_rows, args)
    else:
        # Column weights: filename_stem and preset_name outrank the notes columns,
        # so an organism named in the filename still sorts above one buried in prose.
        sql = f"""
            SELECT {CATALOG_COLUMNS},
                   bm25(preset_fts, 10.0, 10.0, 3.0, 1.0) AS score,
                   (SELECT group_concat(DISTINCT t.label) FROM preset_tag pt
                      JOIN tag t ON t.id = pt.tag_id WHERE pt.preset_id = p.id) AS tags
              FROM preset_fts
              JOIN preset p      ON p.id = preset_fts.rowid
              JOIN source_file s ON s.id = p.source_file_id
              LEFT JOIN author a     ON a.id = p.author_id
              LEFT JOIN collection c ON c.id = p.collection_id
              LEFT JOIN shell sh     ON sh.id = p.shell_id
              LEFT JOIN mode m       ON m.id = p.mode_id
             WHERE preset_fts MATCH ?
        """
        params = [expr]

    for col, val in (("sh.name", args.shell), ("m.token", args.mode),
                     ("a.code", args.author), ("c.name", args.collection)):
        if val:
            sql += f" AND {col} = ?"
            params.append(val)
    if args.from_db:
        sql += (" AND EXISTS (SELECT 1 FROM program pr WHERE pr.preset_id = p.id"
                " AND pr.database_tag = ?)")
        params.append(args.from_db)
    sql += " ORDER BY score LIMIT ?" if not args.regex else " ORDER BY p.filename_stem LIMIT ?"
    params.append(args.limit)

    rows = con.execute(sql, params).fetchall()
    if args.notes:
        sql_notes = sql.replace("SELECT " + CATALOG_COLUMNS + ",",
                                "SELECT " + CATALOG_COLUMNS + ", p.notes_full,")
        rows = con.execute(sql_notes, params).fetchall()
    return emit(rows, args, with_tags=True)


BLACKLIST_HZ = (1840, 1910)   # p140: "believed to cause malignancy growth"
MORTAL_BAND = (76000, 880000)  # p117: Rife/Clark "mortal bandwidth"


def wave_of(params: dict) -> str | None:
    """Which waveform this parameter set selects, if any."""
    for key, name in (
        ("Out1_Inverted_Sawtooth", "InvertedSawtooth"),
        ("Out1_Sawtooth", "Sawtooth"),
        ("Out1_Square_Damped", "SquareDamped"),
        ("Out1_Sine_Damped", "SineDamped"),
        ("Out1_Square_Hbomb", "SquareH-Bomb"),
        ("Out1_Sine_Hbomb", "SineH-Bomb"),
        ("Out1_Square", "Square"),
        ("Out1_Sine", "Sine"),
        ("Out1_Triangle", "Triangle"),
    ):
        if params.get(key) in ("True", "true", True, 1, "1"):
            return name
    return None


def load_shell_table(con) -> dict:
    """Index every shell preset by BOTH its filename stem and its path.

    48,128 of the 48,463 presets declare no waveform of their own and inherit it
    from Base_Preset, which is a backslash path with no extension. Two shapes
    occur in this corpus and both must resolve:

        \\Shell (Empty) Presets\\Remote\\DNA (Dual) (R) - JW   -> by filename
        \\JW_Peptides\\Shells\\Contact                          -> by path
        \\Detox\\Shells\\Killing (R)                            -> by path

    Shells live in three author collections as loose .txt files (JW_Peptides,
    Detox, DH Experimental Frequencies) plus the factory Shell (Empty) Presets
    folder, so the index covers all four.
    """
    rows = con.execute("""
        SELECT p.filename_stem, p.params_json, s.path,
               COALESCE(sh.name,'?') AS shell_name
          FROM preset p
          JOIN source_file s ON s.id = p.source_file_id
          LEFT JOIN shell sh ON sh.id = p.shell_id
         WHERE s.path LIKE '%/Shells/%'
            OR p.collection_id = (SELECT id FROM collection
                                    WHERE name='Shell (Empty) Presets')
    """).fetchall()
    table: dict[str, dict] = {}
    for r in rows:
        try:
            params = json.loads(r["params_json"] or "{}")
        except json.JSONDecodeError:
            params = {}
        entry = {"wave": wave_of(params), "shell": r["shell_name"],
                 "path": r["path"], "params": params}
        table[r["filename_stem"]] = entry
        rel = r["path"][:-4] if r["path"].lower().endswith(".txt") else r["path"]
        table.setdefault(rel, entry)
        table.setdefault(rel.replace("/", "\\"), entry)
    return table


def resolve_chain(base_preset: str | None, shells: dict, depth: int = 4) -> list[str]:
    """Follow Base_Preset up to the shell, reporting each hop."""
    chain: list[str] = []
    seen: set[str] = set()
    current = base_preset
    while current and depth > 0:
        raw = current.strip()
        leaf = raw.replace("\\", "/").split("/")[-1].strip()
        if not leaf or raw in seen:
            break
        seen.add(raw)
        key = next((k for k in (raw.lstrip("\\"), raw, leaf) if k in shells), None)
        if key is not None:
            chain.append(leaf)
            nxt = shells[key]["params"].get("Base_Preset")
            current = nxt if isinstance(nxt, str) else None
        else:
            chain.append(f"{leaf} (not in corpus)")
            break
        depth -= 1
    return chain


def cmd_screen(con, args) -> int:
    """Apply every mechanical rule of the skill in ONE round trip.

    Rules 1, 2 and 6 of SKILL.md are decidable from the database alone. Making the
    model fetch params, frequencies and notes per candidate and evaluate them by
    hand costs ~3 tool calls per row, which for a broad query means well over a
    hundred calls for one question. This command collapses that into a single query
    that returns only what survives, with the reason for anything it drops.
    """
    if args.objective not in ("kill", "heal", "detox", "any"):
        raise SystemExit("--objective must be kill, heal, detox or any")

    # Candidates come from name_fts by rowid, which is exact (see cmd_find).
    sql = f"""
        WITH black AS (
            SELECT DISTINCT pr.preset_id AS pid FROM frequency f
              JOIN program pr ON pr.id = f.program_id
             WHERE f.hz_lo IN ({",".join(str(h) for h in BLACKLIST_HZ)})
        ), cov AS (
            -- How much of each preset the blacklist rule could actually inspect.
            -- A frequency the parser cannot turn into Hz is invisible to `black`,
            -- so a preset can look clean purely because nothing was checkable.
            SELECT pr.preset_id AS pid,
                   COUNT(*)                                          AS freq_rows,
                   SUM(CASE WHEN f.hz_lo IS NULL THEN 1 ELSE 0 END) AS unresolvable
              FROM frequency f JOIN program pr ON pr.id = f.program_id
             GROUP BY pr.preset_id
        )
        SELECT p.id, p.filename_full, p.filename_stem, p.preset_name,
               COALESCE(sh.name,'?') AS shell, p.freq_count, p.program_count,
               p.notes_len, p.description,
               (CASE WHEN b.pid IS NOT NULL THEN 1 ELSE 0 END) AS blacklisted,
               COALESCE(c.freq_rows,0)                         AS freq_rows,
               COALESCE(c.unresolvable,0)                      AS unresolvable,
               json_extract(p.params_json,'$.Frequency_Multiplier')  AS freq_mult,
               json_extract(p.params_json,'$.Out1_Min_Freq')        AS min_freq,
               json_extract(p.params_json,'$.Out1_Max_Freq')        AS max_freq,
               json_extract(p.params_json,'$.Out1_Amplitude')      AS amp,
               json_extract(p.params_json,'$.Out1_Offset')         AS offset,
               json_extract(p.params_json,'$.Out1_Inverted_Sawtooth') AS inv_saw,
               json_extract(p.params_json,'$.Out1_Sawtooth')        AS saw,
               json_extract(p.params_json,'$.Out1_Square')         AS square,
               json_extract(p.params_json,'$.Out1_Sine')           AS sine,
               json_extract(p.params_json,'$.Out1_Triangle')       AS triangle,
               json_extract(p.params_json,'$.Remove_Duplicate_Frequencies') AS dedupe,
               json_extract(p.params_json,'$.Out1_Amplitude') IS NOT NULL AS has_amp,
               p.flags_json, p.base_preset, s.path AS path,
               (SELECT group_concat(DISTINCT t.label) FROM preset_tag pt
                  JOIN tag t ON t.id=pt.tag_id WHERE pt.preset_id=p.id) AS tags
          FROM name_fts
          JOIN preset p      ON p.id = name_fts.rowid
          JOIN source_file s ON s.id = p.source_file_id
          LEFT JOIN shell sh ON sh.id = p.shell_id
          LEFT JOIN mode m  ON m.id = p.mode_id
          LEFT JOIN black b ON b.pid = p.id
          LEFT JOIN cov   c ON c.pid = p.id
         WHERE name_fts MATCH ?
    """
    params: list = [fts_query(args.query)]
    for col, val in (("sh.name", args.shell), ("m.token", args.mode)):
        if val:
            sql += f" AND {col} = ?"
            params.append(val)
    sql += " LIMIT ?"
    params.append(min(args.limit, 500))

    rows = con.execute(sql, params).fetchall()
    shells = load_shell_table(con)
    results = []
    for r in rows:
        flags = json.loads(r["flags_json"] or "{}")
        reasons: list[str] = []
        verdict = "OK"

        if r["blacklisted"]:
            verdict = "REJECT"
            reasons.append(f"contains {BLACKLIST_HZ[0]} Hz (p140 malignancy blacklist)")

        if args.objective == "heal":
            if r["freq_mult"] not in (None, "1", 1):
                verdict = "REJECT"
                reasons.append("Frequency_Multiplier present: killing primitive only (p107)")
            if flags.get("is_sweep"):
                verdict = "REJECT"
                reasons.append("sweep does not heal, it kills (p40)")

        if r["shell"] == "Contact" and r["freq_count"] and r["freq_count"] >= 1000:
            verdict = "FLAG" if verdict == "OK" else verdict
            reasons.append("wide-spectrum on Contact: 20V/1024 = 0.0195 V, no good (p185)")
        if r["min_freq"] not in (None, 0, "0"):
            verdict = "FLAG" if verdict == "OK" else verdict
            reasons.append(f"frequency limit active ({r['min_freq']}): emits freqs NOT in the "
                           f"program list, in the {MORTAL_BAND[0]}-{MORTAL_BAND[1]} Hz band (p118)")
        if r["amp"] not in (None,) and r["offset"] not in (None, 0, "0"):
            verdict = "FLAG" if verdict == "OK" else verdict
            reasons.append(f"offset {r['offset']} reduces real Vpp: amplitude {r['amp']} is "
                           f"not {r['amp']} Vpp (p175)")
        if r["dedupe"] in ("True", "true", 1) and flags.get("is_chain"):
            verdict = "REJECT"
            reasons.append("Remove Duplicate Frequencies on a chain: duplicates are deliberate (p107)")
        if r["shell"] == "Contact":
            verdict = "FLAG" if verdict == "OK" else verdict
            reasons.append("Contact: 7 min zapping cap, 21 min rest (p208)")

        wave = ("InvertedSawtooth" if r["inv_saw"] in ("True", "true", 1) else
                "Sawtooth" if r["saw"] in ("True", "true", 1) else
                "Square" if r["square"] in ("True", "true", 1) else
                "Sine" if r["sine"] in ("True", "true", 1) else
                "Triangle" if r["triangle"] in ("True", "true", 1) else None)
        inherited = ""
        if wave is None and r["base_preset"]:
            chain = resolve_chain(r["base_preset"], shells)
            if chain and chain[-1] in shells:
                sh_wave = shells[chain[-1]]["wave"]
                inherited = chain[-1]
                if sh_wave:
                    wave = sh_wave
                    reasons.append(f"waveform {sh_wave} inherited from shell "
                                   f"'{chain[-1]}'")
                    if sh_wave == "InvertedSawtooth":
                        reasons.append("Inverse Sawtooth = killing waveform (p169)")
                else:
                    reasons.append(f"shell '{chain[-1]}' declares no waveform either")
            else:
                reasons.append(f"Base_Preset chain unresolved: "
                               f"{' -> '.join(chain) if chain else '(empty)'}")
        elif wave == "InvertedSawtooth":
            reasons.append("Inverse Sawtooth = killing waveform (p169)")
        elif wave is None:
            reasons.append("waveform not declared and no Base_Preset to inherit from")

        results.append((verdict, r, reasons, wave, inherited))

    # Coverage is reported last so it never overrides a hard verdict. It only
    # degrades a clean OK, because REJECT is decided from data we did read and
    # a FLAG already says "look closer".
    for i, (verdict, r, reasons, wave, inherited) in enumerate(results):
        if verdict != "OK":
            continue
        checked = (r["freq_rows"] or 0) - (r["unresolvable"] or 0)
        total = r["freq_rows"] or 0
        if total == 0:
            results[i] = ("NO-CHECK", r, reasons + [
                "no frequency rows: nothing was screened for the blacklist"], wave, inherited)
        elif checked == 0:
            results[i] = ("NO-CHECK", r, reasons + [
                f"0 of {total} frequencies could be resolved to Hz, so the "
                f"{BLACKLIST_HZ[0]}/{BLACKLIST_HZ[1]} Hz blacklist was NOT checked at all",
                "this preset is not known to be clean; it is unchecked"],
                wave, inherited)
        elif r["unresolvable"]:
            pct = round(100 * r["unresolvable"] / total)
            results[i] = ("OK-PARTIAL", r, reasons + [
                f"blacklist screened on {checked} of {total} frequencies; "
                f"{r['unresolvable']} ({pct}%) could not be resolved to Hz and were NOT checked"],
                wave, inherited)

    if args.only_ok and not args.all_rows:
        results = [x for x in results if x[0] == "OK"]
    order = {"REJECT": 0, "FLAG": 1, "OK": 2, "OK-PARTIAL": 3, "NO-CHECK": 4}
    results.sort(key=lambda x: (order.get(x[0], 9), -x[1]["freq_count"]))

    if args.json:
        print(json.dumps([
            {"id": r["id"], "filename": r["filename_full"], "shell": r["shell"],
             "freq_count": r["freq_count"], "program_count": r["program_count"],
             "verdict": v, "waveform": w, "inherited_from": inh, "reasons": why,
             "tags": r["tags"], "description": (r["description"] or "")[:200],
             "load_path": r["path"]}
            for v, r, why, w, inh in results], indent=2, ensure_ascii=False))
        return 0

    if not results:
        print("no candidates survived")
        return 1
    counts = Counter(v for v, _, _, _, _ in results)
    print(f"screened {len(results)} candidates for objective={args.objective}: "
          + " ".join(f"{k}={v}" for k, v in counts.most_common()))
    for v, r, why, w, inh in results:
        print(f"\n[{v:<6}] {r['id']:>6}  {r['filename_full']}")
        print(f"         {r['shell']:<8} {r['freq_count']:>5}f {r['program_count']:>3}prog"
              f"  wave={w or 'unverified'}" + (f"  (inherited: {inh})" if inh else ""))
        if r["tags"]:
            print(f"         tags: {str(r['tags'])[:110]}")
        if r["description"]:
            print(f"         desc: {r['description'][:150]}")
        for x in why:
            print(f"         - {x}")
        print(f"         load it: Presets tab > {r['path']}")
    return 0


def cmd_get(con, args) -> int:
    row = con.execute(f"""
        SELECT {CATALOG_COLUMNS}, p.notes_full, p.notes_lead, p.base_preset,
               p.schedule_run_for, p.repeat_sequence, p.params_json, p.flags_json
          FROM preset p
          JOIN source_file s ON s.id = p.source_file_id
          LEFT JOIN author a     ON a.id = p.author_id
          LEFT JOIN collection c ON c.id = p.collection_id
          LEFT JOIN shell sh     ON sh.id = p.shell_id
          LEFT JOIN mode m       ON m.id = p.mode_id
         WHERE p.id = ?
    """, (args.preset_id,)).fetchone()
    if row is None:
        raise SystemExit(f"no preset with id {args.preset_id}")

    # params_json is KEPT: it carries Frequency_Multiplier, Dwell_Multiplier and
    # the Out1_* waveform keys, which are exactly the mechanism signals the skill
    # reasons over. Only the prose blob is gated behind --notes.
    out: dict = {"preset": {k: row[k] for k in row.keys() if k != "notes_full"}}
    if not args.notes:
        out["preset"].pop("notes_full", None)

    out["tags"] = [dict(r) for r in con.execute(
        "SELECT t.slug, t.label, t.category, pt.source, pt.evidence FROM preset_tag pt"
        " JOIN tag t ON t.id=pt.tag_id WHERE pt.preset_id=? ORDER BY pt.confidence DESC",
        (args.preset_id,))]
    out["durations"] = [dict(r) for r in con.execute(
        "SELECT kind, value_text, minutes FROM preset_duration WHERE preset_id=?",
        (args.preset_id,))]
    out["flags"] = json.loads(row["flags_json"]) if row["flags_json"] else {}
    out["warnings"] = [dict(r) for r in con.execute(
        "SELECT kind, evidence FROM preset_warning WHERE preset_id=?", (args.preset_id,))]
    out["programs"] = [dict(r) for r in con.execute(
        "SELECT ordinal, program_name FROM program WHERE preset_id=? ORDER BY ordinal",
        (args.preset_id,))]

    if args.freqs:
        out["frequencies"] = [dict(r) for r in con.execute(
            "SELECT program_ordinal, freq_ordinal, notation, raw_token, hz_lo, hz_hi,"
            " amplitude, modifiers, codes, parse_status FROM v_freq_lookup"
            " WHERE preset_id=? ORDER BY program_ordinal, freq_ordinal",
            (args.preset_id,))]
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def cmd_tags(con, args) -> int:
    if args.slug:
        rows = con.execute(
            "SELECT t.slug, t.label, t.category, COUNT(*) AS n FROM tag t"
            " JOIN preset_tag pt ON pt.tag_id=t.id WHERE t.slug=? GROUP BY 1 ORDER BY n DESC",
            (args.slug,)).fetchall()
        print(f"{rows[0]['label']} ({rows[0]['slug']}): {rows[0]['n']:,} presets\n" if rows else "no presets\n")
        sql = f"""
            SELECT {CATALOG_COLUMNS}
              FROM preset p
              JOIN source_file s ON s.id = p.source_file_id
              JOIN preset_tag pt ON pt.preset_id = p.id
              JOIN tag t ON t.id = pt.tag_id
              LEFT JOIN author a     ON a.id = p.author_id
              LEFT JOIN collection c ON c.id = p.collection_id
              LEFT JOIN shell sh     ON sh.id = p.shell_id
              LEFT JOIN mode m       ON m.id = p.mode_id
             WHERE t.slug = ? ORDER BY p.author_id, p.filename_stem LIMIT ?
        """
        return emit(con.execute(sql, (args.slug, args.limit)).fetchall(), args)
    rows = con.execute(
        "SELECT category, slug, label, COUNT(*) AS n FROM tag t"
        " LEFT JOIN preset_tag pt ON pt.tag_id=t.id GROUP BY t.id ORDER BY category, n DESC"
    ).fetchall()
    return emit(rows, args)


def cmd_freqs(con, args) -> int:
    sql = f"""
        SELECT {CATALOG_COLUMNS}, vf.program_ordinal, vf.notation, vf.raw_token,
               vf.hz_lo, vf.hz_hi, vf.amplitude, vf.modifiers, vf.codes
          FROM v_freq_lookup vf
          JOIN preset p ON p.id = vf.preset_id
          JOIN source_file s ON s.id = p.source_file_id
          LEFT JOIN author a     ON a.id = p.author_id
          LEFT JOIN collection c ON c.id = p.collection_id
          LEFT JOIN shell sh     ON sh.id = p.shell_id
          LEFT JOIN mode m       ON m.id = p.mode_id
         WHERE 1=1
    """
    params: list = []
    if args.hz is not None:
        sql += " AND (vf.hz_lo BETWEEN ? AND ?)"
        params += [args.hz - args.tolerance, args.hz + args.tolerance]
    sql += " ORDER BY vf.hz_lo LIMIT ?"
    params.append(args.limit)
    return emit(con.execute(sql, params).fetchall(), args)


def cmd_stats(con, args) -> int:
    out = {
        "presets": con.execute("SELECT COUNT(*) FROM preset").fetchone()[0],
        "programs": con.execute("SELECT COUNT(*) FROM program").fetchone()[0],
        "frequencies": con.execute("SELECT COUNT(*) FROM frequency").fetchone()[0],
        "with_description": con.execute(
            "SELECT COUNT(*) FROM preset WHERE has_description=1").fetchone()[0],
        "by_shell": dict(con.execute(
            "SELECT COALESCE(sh.name,'(none)'), COUNT(*) FROM preset p"
            " LEFT JOIN shell sh ON sh.id=p.shell_id GROUP BY 1 ORDER BY 2 DESC").fetchall()),
        "by_author": dict(con.execute(
            "SELECT COALESCE(a.code,'(none)'), COUNT(*) FROM preset p"
            " LEFT JOIN author a ON a.id=p.author_id GROUP BY 1 ORDER BY 2 DESC").fetchall()),
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def emit(rows, args, with_tags: bool = False) -> int:
    if not rows:
        print("no matches")
        return 1
    if args.json:
        print(json.dumps([dict(r) for r in rows], indent=2, ensure_ascii=False))
        return 0
    for r in rows:
        line = (f"{r['id']:>6}  {r['filename_full']}"
                if "id" in r.keys() else f"{r['slug']:<24} {r['n']:>7,}")
        print(line)
        for key, label in (("author", "by"), ("shell", "shell"), ("mode", "mode"),
                           ("collection", "in"), ("description", "desc"),
                           ("matched_programs", "MATCHED"),
                           ("tags", "tags"), ("notation", "notation"),
                           ("raw_token", "freq"), ("hz_lo", "hz"),
                           ("program_count", "programs"), ("freq_count", "freqs"),
                           ("path", "path"), ("category", "cat"), ("n", "count")):
            if key in r.keys() and r[key] not in (None, ""):
                value = str(r[key])
                if len(value) > args.width:
                    value = value[: args.width - 3] + "..."
                pad = 9 if key == "description" else 5
                print(f"{'':{pad}}{label}: {value}")
        print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    # Shared flags are attached to the top level AND to every subcommand, so both
    # `query.py --limit 5 find x` and `query.py find x --limit 5` work. A skill
    # should not have to remember argument order.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", default=DEFAULT_DB)
    common.add_argument("--limit", type=int, default=10)
    common.add_argument("--width", type=int, default=150)
    common.add_argument("--json", action="store_true")
    common.add_argument("--notes", action="store_true", help="include full notes (expensive)")
    common.add_argument("--freqs", action="store_true", help="include frequency rows (expensive)")
    common.add_argument("--shell", help="Coil, Contact, Plasma, Remote, Scalar, Laser, Footbath")
    common.add_argument("--mode", help="R, C, L, SS, P, Coil, Dual, GX, XM, FB")
    common.add_argument("--author", help="JW, EL, DB, BY, ...")
    common.add_argument("--collection", help="DNA, Detox, Cancer, ...")
    common.add_argument("--from-db", dest="from_db", metavar="TAG",
                        help="only presets whose programs come from this Spooky2 "
                             "database: ALT BFB BIO CAFL CUST DNA ETDFL HC KHZ MW "
                             "PROV RIFE RRM RUSS SD VEGA XTRA. Run 'dbinfo' for what "
                             "each one means and how many this corpus has.")
    common.add_argument("--regex", action="store_true",
                        help="treat the query as a regex over filename AND PresetName")
    common.add_argument("--in", dest="in_", choices=["all", "names", "notes", "programs"],
                        default="all",
                        help="all: names + author prose, names ranked first (default). "
                             "names: filenames and PresetName only. "
                             "notes: force prose-only matching. "
                             "programs: DEEP SEARCH by subprogram name, always showing "
                             "which program matched. Use when a title understates what "
                             "a preset actually treats.")

    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("find", parents=[common]); p.set_defaults(fn=cmd_find)
    p.add_argument("query")
    p = sub.add_parser("get", parents=[common]); p.set_defaults(fn=cmd_get)
    p.add_argument("preset_id", type=int)
    p = sub.add_parser("tags", parents=[common]); p.set_defaults(fn=cmd_tags)
    p.add_argument("slug", nargs="?")
    p = sub.add_parser("freqs", parents=[common]); p.set_defaults(fn=cmd_freqs)
    p.add_argument("--hz", type=float); p.add_argument("--tolerance", type=float, default=0.5)
    sub.add_parser("stats", parents=[common]).set_defaults(fn=cmd_stats)
    sub.add_parser("dbinfo", parents=[common]).set_defaults(fn=cmd_dbinfo)
    p = sub.add_parser("screen", parents=[common]); p.set_defaults(fn=cmd_screen)
    p.add_argument("query")
    p.add_argument("--objective", choices=["kill", "heal", "detox", "any"], default="any",
                   help="which objective to apply the kill/heal rejections for")
    p.add_argument("--only-ok", action="store_true",
                   help="hide rejected rows, keep only clean candidates")
    p.add_argument("--all", dest="all_rows", action="store_true",
                   help="show every candidate including rejected, with reasons")
    return ap


def main() -> int:
    args = build_parser().parse_args()
    return args.fn(connect(args.db), args)


if __name__ == "__main__":
    raise SystemExit(main())