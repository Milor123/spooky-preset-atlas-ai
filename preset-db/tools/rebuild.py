"""Rebuild the preset database after a Spooky2 update, and report what changed.

Spooky2 ships new preset material with releases (the JW Peptide collection landed
in 2026 and was entirely new). When that happens this script rebuilds the index
from whatever the installer currently contains and prints a diff against the
existing database, so you can see what arrived and what left.

Design rules
------------
* **Never destroys the current database.** The new one is written beside it as
  spooky-NEW.db. Promoting it is a separate, explicit `--swap`.
* **Never hardcodes a path.** Discovers the corpus via --corpus, then the
  SPOOKY2_CORPUS environment variable, then the usual install locations. That way
  it still works after a Windows reinstall or a move to another drive.
* **Skips Preset Collections/User by default.** Those are your own presets. Index
  them with --include-user if you want them searchable too.
* **Runs the audit** before anything is promoted. A rebuild that fails the audit
  does not replace a database that passed.

Usage
    python rebuild.py                    discover, build to spooky-NEW.db, audit, diff
    python rebuild.py --report-only      diff only, build nothing (needs a prior --build)
    python rebuild.py --corpus "S:\\Spooky2\\Preset Collections"
    python rebuild.py --include-user     also index your personal presets
    python rebuild.py --swap             promote the new db after reviewing the diff
"""

from __future__ import annotations

import argparse
import datetime
import os
import shutil
import sqlite3
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DB_ROOT = os.path.dirname(HERE)
BUILD_DIR = os.path.join(DB_ROOT, "build")
CURRENT = os.path.join(BUILD_DIR, "spooky.db")
CANDIDATE = os.path.join(BUILD_DIR, "spooky-NEW.db")


# ---------------------------------------------------------------------------
# diff
# ---------------------------------------------------------------------------

def snapshot(path: str) -> dict:
    """Everything worth comparing between two builds."""
    if not os.path.exists(path):
        return {}
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    out: dict = {}
    out["collections"] = dict(con.execute(
        "SELECT name, preset_count FROM collection ORDER BY name").fetchall())
    out["shells"] = dict(con.execute(
        "SELECT COALESCE(name,'(none)'), COUNT(*) FROM shell s"
        " LEFT JOIN preset p ON p.shell_id=s.id GROUP BY 1").fetchall())
    out["authors"] = dict(con.execute(
        "SELECT COALESCE(code,'(none)'), COUNT(*) FROM author a"
        " LEFT JOIN preset p ON p.author_id=a.id GROUP BY 1").fetchall())
    out["files"] = {p: h for p, h in con.execute(
        "SELECT path, content_hash FROM source_file")}
    out["counts"] = {
        "files": con.execute("SELECT COUNT(*) FROM source_file").fetchone()[0],
        "presets": con.execute("SELECT COUNT(*) FROM preset").fetchone()[0],
        "programs": con.execute("SELECT COUNT(*) FROM program").fetchone()[0],
        "frequencies": con.execute("SELECT COUNT(*) FROM frequency").fetchone()[0],
        "keys": con.execute(
            "SELECT COUNT(*) FROM (SELECT 1 FROM preset, json_each(preset.params_json)"
            " GROUP BY json_each.key)").fetchone()[0] if True else 0,
        "notes_mb": round((con.execute(
            "SELECT COALESCE(SUM(LENGTH(CAST(notes_full AS BLOB))),0)"
            " FROM preset").fetchone()[0]) / 1e6, 1),
    }
    con.close()
    return out


def diff(old: dict, new: dict, show: int = 30) -> dict:
    if not old:
        return {"note": "no previous database to compare against"}
    added = sorted(set(new["files"]) - set(old["files"]))
    removed = sorted(set(old["files"]) - set(new["files"]))
    modified = sorted(p for p in (set(old["files"]) & set(new["files"]))
                      if old["files"][p] != new["files"][p])

    def by_collection(paths, snap):
        agg: dict[str, int] = {}
        for p in paths:
            coll = p.split("/")[0]
            agg[coll] = agg.get(coll, 0) + 1
        return dict(sorted(agg.items(), key=lambda kv: -kv[1]))

    summary: dict = {
        "files": {k: (old["counts"][k], new["counts"][k]) for k in old["counts"]},
        "added_files": len(added),
        "removed_files": len(removed),
        "modified_files": len(modified),
        "added_by_collection": by_collection(added, new),
        "removed_by_collection": by_collection(removed, old),
        "new_collections": sorted(set(new["collections"]) - set(old["collections"])),
        "gone_collections": sorted(set(old["collections"]) - set(new["collections"])),
        "new_authors": sorted(set(new["authors"]) - set(old["authors"])),
        "gone_authors": sorted(set(old["authors"]) - set(new["authors"])),
    }
    lines = []
    lines.append("=" * 70)
    lines.append("  DIFF against the current database")
    lines.append("=" * 70)
    lines.append(f"  built {datetime.datetime.now():%Y-%m-%d %H:%M}")
    lines.append("")
    lines.append("  metric                 before        after        delta")
    for k, (o, n) in summary["files"].items():
        d = (n - o) if isinstance(o, (int, float)) and isinstance(n, (int, float)) else ""
        lines.append(f"  {k:<22}{o:>10,}    {n:>10,}    {d:>+10,}")
    lines.append("")
    lines.append(f"  files added     {summary['added_files']:>8,}")
    lines.append(f"  files modified  {summary['modified_files']:>8,}")
    lines.append(f"  files removed   {summary['removed_files']:>8,}")
    if added:
        lines.append("")
        lines.append(f"  ADDED, by collection ({len(added)} total, top {show}):")
        for coll, n in list(summary["added_by_collection"].items())[:12]:
            lines.append(f"    {n:>6,}  {coll}")
        for p in added[:show]:
            lines.append(f"        + {p}")
        if len(added) > show:
            lines.append(f"        ... and {len(added) - show} more")
    if removed:
        lines.append("")
        lines.append(f"  REMOVED ({len(removed)} total, top {show}):")
        for p in removed[:show]:
            lines.append(f"        - {p}")
        if len(removed) > show:
            lines.append(f"        ... and {len(removed) - show} more")
    if modified:
        lines.append("")
        lines.append(f"  MODIFIED content ({len(modified)}, top {show}):")
        for p in modified[:show]:
            lines.append(f"        ~ {p}")
    if summary["new_collections"] or summary["gone_collections"]:
        lines.append("")
        lines.append(f"  new collections  : {summary['new_collections'] or 'none'}")
        lines.append(f"  gone collections : {summary['gone_collections'] or 'none'}")
    if summary["new_authors"]:
        lines.append("")
        lines.append(f"  new authors      : {summary['new_authors']}")
    summary["report"] = "\n".join(lines)
    return summary


# ---------------------------------------------------------------------------
# build + audit + promote
# ---------------------------------------------------------------------------

def run_audit(db_path: str) -> bool:
    proc = subprocess.run([sys.executable, os.path.join(HERE, "audit.py"), db_path],
                          capture_output=True, text=True)
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print(proc.stderr.strip()[-600:])
    return proc.returncode == 0


def do_swap() -> None:
    if not os.path.exists(CANDIDATE):
        raise SystemExit(f"nothing to promote: {CANDIDATE} does not exist")
    backup = CURRENT + f".{datetime.date.today():%Y%m%d}.bak"
    shutil.copy2(CURRENT, backup)
    shutil.move(CANDIDATE, CURRENT)
    for suffix in ("-wal", "-shm"):
        if os.path.exists(CURRENT + suffix):
            os.remove(CURRENT + suffix)
    print(f"\n  promoted {os.path.basename(CANDIDATE)} -> {os.path.basename(CURRENT)}")
    print(f"  previous database kept as {os.path.basename(backup)}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", help="path to Preset Collections (default: auto-detect)")
    ap.add_argument("--include-user", action="store_true",
                    help="also index Preset Collections/User (your own presets)")
    ap.add_argument("--report-only", action="store_true",
                    help="diff an existing spooky-NEW.db, build nothing")
    ap.add_argument("--swap", action="store_true",
                    help="promote spooky-NEW.db to spooky.db after a clean audit")
    ap.add_argument("--build", action="store_true",
                    help="force a rebuild even if spooky-NEW.db exists")
    args = ap.parse_args()

    if args.swap:
        if args.report_only:
            raise SystemExit("--swap and --report-only are mutually exclusive")
        if not run_audit(CANDIDATE):
            raise SystemExit("\n  the candidate database FAILED the audit; not promoting it")
        do_swap()
        return 0

    if args.report_only:
        new = snapshot(CANDIDATE)
        if not new:
            raise SystemExit(f"no candidate database at {CANDIDATE}")
        print(diff(snapshot(CURRENT), new)["report"])
        return 0

    if not os.path.exists(CURRENT):
        print("no current database; this will be the first build")

    t0 = time.time()
    print(f"building {os.path.basename(CANDIDATE)} ...\n")
    subprocess.run([sys.executable, os.path.join(HERE, "build_db.py"), "--full",
                    "--db", CANDIDATE, "--corpus", args.corpus or "",
                    *(["--include-user"] if args.include_user else [])], check=True)

    print(f"\nauditing the candidate ...\n")
    if not run_audit(CANDIDATE):
        print(f"\n  the candidate FAILED the audit. It was left at {CANDIDATE}")
        print("  your current database is untouched.")
        return 1

    summary = diff(snapshot(CURRENT), snapshot(CANDIDATE))
    print(summary.get("report", ""))
    print()
    if summary.get("added_files") or summary.get("modified_files"):
        print(f"  candidate left at {os.path.basename(CANDIDATE)}")
        print("  review the diff, then run:  python rebuild.py --swap")
    else:
        print("  no change. the candidate is identical in content.")
        os.remove(CANDIDATE)
    print(f"  total {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())