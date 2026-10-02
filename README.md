# Spooky Preset Atlas

**An AI skill and local index of 48,463 frequency presets.** Remote, Contact,
Plasma, Scalar, Coil and Cold Laser, across bacteria, viruses, parasites, fungi
and detox protocols. A Pi skill uses it to choose what to run, instead of anyone
reading 43,397 files by hand.

> **Not affiliated with, endorsed by, or sponsored by The Spooky Team or any
> other preset vendor.** "Spooky" is used here as an ordinary English adjective,
> not as a product mark. This repository contains only the indexing engine and
> an AI skill. It redistributes no presets, no notes and no vendor
> documentation; each user builds their own index from their own licensed copy.
> See *What is deliberately absent* below.

Presets are not medical claims. This tool helps you choose among programs that
already exist; it does not diagnose, and it does not present the claims of
preset authors as fact.

## What is in here

```
preset-db/schema/schema.sql      the database schema
preset-db/tools/                 build, query, audit, rebuild
preset-db/docs/KNOWLEDGE.md      consolidated User's Guide knowledge, with page citations
preset-db/docs/notes/            raw visual-read notes of the guide pages
skills/spooky2-presets/SKILL.md  the Pi skill (see its README for install)
```

The database itself, the corpus, and the User's Guide are **not** in this
repository. See *What is deliberately absent* below.

## Quick start

```bash
python preset-db/tools/build_db.py --full    # ~2-4 min, ~3 GB RAM
python preset-db/tools/audit.py              # independent verification
python preset-db/tools/query.py dbinfo
```

Point it at your own corpus if it is not in the default place:

```bash
python preset-db/tools/build_db.py --full --presets "S:\Spooky2\Preset Collections"
```

## Querying

```bash
python preset-db/tools/query.py find "parasite" --limit 5
python preset-db/tools/query.py screen "cancer" --shell Contact --limit 5
python preset-db/tools/query.py get 12345 --notes --freqs
```

`screen` applies the mechanical safety rules in a single call, which is what the
skill uses before it recommends anything.

## Requirements

- Python 3.9+ (standard library only, no third-party packages)
- ~2-4 GB of free RAM **to build**; querying needs 3–23 MB and under a second

## What is deliberately absent

This repository contains the **engine**, not the data.

- **The database** is a build artifact. It is regenerable in minutes, so it is
  gitignored rather than committed.
- **`Preset Collections/`** is the user's own copy of The Spooky Team's corpus.
  It is not ours to redistribute, and it is rebuilt from their own install.
- **The User's Guide PDF** is copyrighted. `KNOWLEDGE.md` is our own summary of
  it, cited by page.
- **`Prueba-secreta/`** was reverse-engineering work on Spooky2's encrypted
  database and is out of scope.
- **`DatabaseText.txt`** is Spooky2's own export of its program catalog. It is
  not ingested: it resolves only about 2% of the programs that presets actually
  reference, because almost all of those are custom programs written by preset
  authors rather than factory entries.

Anyone with a licensed copy of Spooky2 can build the same database from it.

## A note on safety

The safety caps enforced by `screen` come from the vendor's own user guide and
are not negotiable; the skill is instructed never to soften them. If a preset
violates a cap, the answer is a different preset, not a shorter session.

Contact delivery on this hardware runs at 14–20 V against 4–10 V for Remote, and
is the highest-power mode available. Two frequencies are treated as a blacklist
in the skill: **1840 Hz** (83 occurrences across 22 presets) and **1910 Hz**.
See `preset-db/docs/KNOWLEDGE.md` for the full set with page citations.
