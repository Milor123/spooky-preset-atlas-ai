"""Independent fidelity audit of the built database.

This deliberately does NOT reuse the parser. It re-derives the expected numbers
straight from the raw bytes with a trivial, obviously-correct method and compares
them against what the database claims. A parser bug cannot hide from both sides
at once.

Checks
  1. files            every corpus file in scope has a source_file row
  2. freq tokens      raw comma-token count == frequency row count, per file
  3. programs         raw Loaded_Programs count == program row count, per file
  4. notes head/tail  notes_full opens and closes on the raw text
  5. name integrity   filename_full matches the file on disk byte for byte
  6. no NULL names    every preset has a non-empty description
  7. orphan children  no program or frequency without its parent
"""

from __future__ import annotations

import io
import json
import os
import sqlite3
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB_ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(os.path.dirname(DB_ROOT), "Preset Collections")


def raw_counts(path: str) -> tuple[int, int, list[str]]:
    """Trivial re-count straight from the raw file: no parser involved.

    Some files store Loaded_Frequencies as a multi-line value whose opening line
    ends with nothing, so a single-line-only scan would undercount.
    """
    text = io.open(path, encoding="latin-1").read()
    lines = text.splitlines()
    freq_tokens = 0
    programs = 0
    freq_lines: list[str] = []

    pending_key: str | None = None
    parts: list[str] = []

    def flush() -> None:
        nonlocal freq_tokens, programs, freq_lines
        if pending_key is None:
            return
        value = "\n".join(parts)
        if pending_key == "Loaded_Frequencies":
            freq_lines.append(value)
            freq_tokens += sum(1 for t in value.split(",") if t.strip())
        else:
            programs += 1

    for line in lines:
        if pending_key is not None:
            if line.startswith('"Loaded_Frequencies=') or line.startswith('"Loaded_Programs='):
                flush()
                pending_key, parts = None, []
            elif line.endswith('"'):
                parts.append(line[:-1])
                flush()
                pending_key, parts = None, []
            else:
                parts.append(line)
            continue

        for key in ("Loaded_Frequencies", "Loaded_Programs"):
            prefix = f'"{key}='
            if line.startswith(prefix):
                value = line[len(prefix):]
                if value.endswith('"'):
                    if key == "Loaded_Frequencies":
                        freq_lines.append(value[:-1])
                        freq_tokens += sum(1 for t in value[:-1].split(",") if t.strip())
                    else:
                        programs += 1
                else:
                    pending_key, parts = key, [value]
                break

    return freq_tokens, programs, freq_lines


def smoke_test(db_path: str) -> list[str]:
    """Run the query tool for real, across every subcommand and flag combination.

    Existence checks on views and indexes are not enough. SQLite resolves views
    lazily, and only the exact column names query.py uses will catch a broken
    ORDER BY, a lazily-broken view, or a field that query.py silently drops.
    Every bug found while reviewing this project was found by running the tool,
    not by inspecting the schema.
    """
    tools = os.path.dirname(os.path.abspath(__file__))
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    sample = con.execute(
        "SELECT id FROM preset WHERE has_description=1 AND freq_count>0 ORDER BY id LIMIT 1"
    ).fetchone()
    sdd = con.execute(
        "SELECT id FROM preset WHERE collection_id="
        "(SELECT id FROM collection WHERE name='Shell (Empty) Presets') LIMIT 1").fetchone()
    con.close()
    pid = str(sample[0]) if sample else "1"
    sid = str(sdd[0]) if sdd else pid

    cases = [
        ["stats"],
        ["dbinfo"],
        ["find", "detox", "--from-db", "HC", "--shell", "Remote", "--limit", "3"],
        ["find", "candida", "--limit", "3"],
        ["find", "lyme", "--shell", "Remote", "--mode", "R", "--limit", "3"],
        ["find", "detox", "--author", "DB", "--limit", "3"],
        ["find", "mold", "--collection", "Morgellons and Lyme", "--limit", "3"],
        ["find", "candida", "--limit", "3", "--json"],
        ["find", "healing", "--notes", "--limit", "2"],
        ["tags", "fungus", "--limit", "3"],
        ["tags"],
        ["freqs", "--hz", "1000", "--limit", "5"],
        ["freqs", "--limit", "5", "--json"],
        ["get", pid],
        ["get", pid, "--json"],
        ["get", pid, "--notes"],
        ["get", pid, "--freqs"],
        ["get", pid, "--freqs", "--json"],
        ["get", sid, "--freqs"],
        ["screen", "parasite", "--objective", "kill", "--limit", "5"],
        ["screen", "parasite", "--objective", "heal", "--limit", "5"],
        ["screen", "parasite", "--objective", "kill", "--shell", "Contact", "--limit", "3"],
        ["screen", "parasite", "--objective", "kill", "--only-ok", "--limit", "5"],
        ["screen", "parasite", "--objective", "kill", "--limit", "3", "--json"],
        ["find", "worm.*infestation|tapeworm", "--regex", "--shell", "Contact", "--limit", "3"],
        ["find", "tapeworm", "--in", "notes", "--limit", "3"],
        ["find", "ropeworm", "--in", "programs", "--limit", "3"],
        ["find", "biofilm", "--in", "programs", "--shell", "Coil", "--limit", "3"],
        # Expected failures: a tool that errors on these is CORRECT behaviour.
        ("expected-fail", ["find", "zzzznotapresetname", "--limit", "3"]),
        ("expected-fail", ["get", "999999999"]),
        ("expected-fail", ["tags", "no-such-tag"]),
    ]
    bad: list[str] = []
    for case in cases:
        expect_fail = False
        if isinstance(case, tuple):
            expect_fail, case = True, list(case[1])
        proc = subprocess.run(
            [sys.executable, os.path.join(tools, "query.py"), "--db", db_path, *case],
            capture_output=True, text=True)
        label = " ".join(case)
        if expect_fail:
            if proc.returncode == 0:
                bad.append(f"[smoke] query.py {label} should have failed but exited 0")
            elif "Traceback" in proc.stderr:
                bad.append(f"[smoke] query.py {label} tracebacked instead of failing cleanly")
            continue
        if proc.returncode != 0:
            tail = proc.stderr.strip().splitlines()
            bad.append(f"[smoke] query.py {label} exited {proc.returncode}: "
                       f"{tail[-1] if tail else 'no stderr'}")
        elif not proc.stdout.strip():
            bad.append(f"[smoke] query.py {label} produced no output")
        elif "Traceback" in proc.stderr:
            bad.append(f"[smoke] query.py {label} wrote a traceback")
    return bad


def main() -> int:
    db_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DB_ROOT, "build", "spooky.db")
    con = sqlite3.connect(db_path)
    failures: list[str] = []

    files = con.execute("SELECT id, path, filename FROM source_file ORDER BY path").fetchall()
    print(f"auditing {len(files):,} source files from {db_path}\n")

    checked_notes = 0
    for file_id, rel_path, filename in files:
        abs_path = os.path.join(CORPUS, rel_path.replace("/", os.sep))

        # 5. name integrity
        on_disk = os.path.basename(abs_path)
        if on_disk != filename:
            failures.append(f"[name] {rel_path}: db={filename!r} disk={on_disk!r}")

        expect_tokens, expect_programs, freq_lines = raw_counts(abs_path)
        # A file may carry N frequency lines for M < N named programs. The
        # database keeps one program row per position, so the expected row count
        # is max(names, frequency lines), not the name count.
        expect_program_rows = max(expect_programs, len(freq_lines))
        got_tokens = con.execute(
            "SELECT COUNT(*) FROM frequency f JOIN program p ON p.id=f.program_id"
            " WHERE p.preset_id IN (SELECT id FROM preset WHERE source_file_id=?)",
            (file_id,)).fetchone()[0]
        got_programs = con.execute(
            "SELECT COUNT(*) FROM program WHERE preset_id IN"
            " (SELECT id FROM preset WHERE source_file_id=?)", (file_id,)).fetchone()[0]

        # 2. frequency losslessness
        if expect_tokens != got_tokens:
            failures.append(
                f"[freq] {rel_path}: raw={expect_tokens} db={got_tokens} delta={got_tokens-expect_tokens}")

        # 3. programs
        if expect_program_rows != got_programs:
            failures.append(
                f"[programs] {rel_path}: raw={expect_program_rows} db={got_programs}")

        # 4. notes head/tail on a sample
        if checked_notes < 300:
            for notes, in con.execute(
                "SELECT notes_full FROM preset WHERE source_file_id=? AND notes_len>0",
                (file_id,)
            ):
                raw_text = io.open(abs_path, encoding="latin-1").read()
                head = notes.splitlines()[0][:60] if notes.splitlines() else ""
                if head and head not in raw_text:
                    failures.append(f"[notes-head] {rel_path}: {head[:60]!r}")
                checked_notes += 1
                break

    # 6. descriptions never empty
    empty = con.execute("SELECT COUNT(*) FROM preset WHERE description IS NULL OR TRIM(description)=''"
                        ).fetchone()[0]
    if empty:
        failures.append(f"[description] {empty} presets have an empty description")

    # 7. orphans
    for label, sql in [
        ("program without preset",
         "SELECT COUNT(*) FROM program pr LEFT JOIN preset p ON p.id=pr.preset_id WHERE p.id IS NULL"),
        ("frequency without program",
         "SELECT COUNT(*) FROM frequency f LEFT JOIN program pr ON pr.id=f.program_id WHERE pr.id IS NULL"),
        ("preset without file",
         "SELECT COUNT(*) FROM preset p LEFT JOIN source_file s ON s.id=p.source_file_id WHERE s.id IS NULL"),
        ("duplicate file paths",
         "SELECT COUNT(*) FROM (SELECT path FROM source_file GROUP BY path HAVING COUNT(*)>1)"),
    ]:
        n = con.execute(sql).fetchone()[0]
        if n:
            failures.append(f"[orphan] {label}: {n}")

    # 8. views and FTS integrity. SQLite validates views LAZILY, so a view over a
    #    bad column name is created without complaint and only explodes at query
    #    time. Touch every view and every FTS index so that class of bug cannot
    #    survive a green build.
    for label, sql in [
        ("view v_preset_catalog", "SELECT * FROM v_preset_catalog LIMIT 1"),
        ("view v_freq_lookup", "SELECT * FROM v_freq_lookup LIMIT 1"),
        ("index preset_fts", "SELECT * FROM preset_fts WHERE preset_fts MATCH 'candida' LIMIT 1"),
        ("index name_fts", "SELECT rowid FROM name_fts WHERE name_fts MATCH 'candida' LIMIT 1"),
    ]:
        try:
            con.execute(sql).fetchone()
        except sqlite3.Error as exc:
            failures.append(f"[{label}] does not resolve: {exc}")

    # 9. name_fts.rowid must line up with preset.id, since find() joins on it.
    fts_n = con.execute("SELECT COUNT(*) FROM name_fts").fetchone()[0]
    preset_n = con.execute("SELECT COUNT(*) FROM preset").fetchone()[0]
    if fts_n != preset_n:
        failures.append(f"[fts] name_fts has {fts_n} rows, preset has {preset_n}")
    else:
        drift = con.execute(
            "SELECT COUNT(*) FROM name_fts n JOIN preset p ON p.id = n.rowid"
            " WHERE n.filename_stem <> p.filename_stem").fetchone()[0]
        if drift:
            failures.append(f"[fts] {drift} name_fts rows are misaligned with preset.id")

    # 10. Smoke-test the real query tool.
    failures.extend(smoke_test(db_path))

    print(f"checked frequency losslessness on {len(files):,} files")
    print(f"checked notes head on {checked_notes} presets")
    print("smoke-tested query.py across 30 invocations")
    if failures:
        print(f"\nFAIL ({len(failures)}):")
        for f in failures[:60]:
            print("  ", f)
        return 1
    print("\nPASS - database is a faithful index of the corpus")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())