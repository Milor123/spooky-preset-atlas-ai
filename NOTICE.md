# NOTICE

This project is MIT licensed. That license covers the **code**. It does not
cover the **data**, and this file explains exactly where the line falls, because
getting that wrong would be dishonest.

## What is ours, and is MIT licensed

Everything in this repository that we wrote:

- `preset-db/schema/schema.sql` — the database design
- `preset-db/tools/spooky/parser.py`, `extract.py` — the parser
- `preset-db/tools/{build_db,query,audit,rebuild,extract_guide}.py` — the tooling
- `skills/spooky2-presets/SKILL.md` — the AI skill, including the safety rules
  we derived from the guide
- The taxonomy, the tag system, the database-tag glossary, and the analysis in
  `preset-db/docs/KNOWLEDGE.md`

## What is not ours, and is not MIT licensed

- The preset corpus itself — 43,397 files belonging to their authors and to
  The Spooky Team
- The Spooky2 User's Guide and every other vendor PDF
- The content of a database built from that corpus: preset names, the
  descriptions, and the frequency lines are the authors' and the vendor's text,
  merely restructured

## What we actually did

Stated plainly, because it matters:

1. We read the **publicly distributed** Spooky 2 User's Guide PDF, page by
   page, and wrote our own summary of it, cited by page number. That summary is
   in `preset-db/docs/KNOWLEDGE.md`. It is our analysis, not their text.
2. We wrote a parser for the `.txt` preset format and built a searchable index
   from **a licensed copy of Spooky2 that the user already owned**. Nothing was
   downloaded from anywhere, and no copy of the corpus is redistributed here.
3. We did not touch, and cannot read, the encrypted frequency database. Spooky2
   states of it: *"The ZIP format we use is encrypted, cannot be manually
   unzipped, and cannot be read by any software but Spooky2. This is to help
   prevent third-party profiteering on planned future frequency development."*
   We have no interest in defeating that, and the tooling here does not attempt
   it. Frequencies in the index come only from the plaintext of the user's own
   preset files.

## The vendor's own license statement

Spooky2's User's Guide, page 242, states:

> "Although the source code is © John White, this software is free … You are
> actively encouraged to pass it on freely to everyone you know, as long as it's
> accompanied by this document."

That is a statement about **their software**, and it is theirs to grant. It is
not a license to the presets, and we are not redistributing their software.

## What you must do to use the data

The database is a build artifact and is not in this repository. To build it you
need your own licensed copy of Spooky2. Then:

```bash
python preset-db/tools/build_db.py --full --presets "<your path to Preset Collections>"
```

The resulting database is yours. It contains your vendor's and your authors'
content, so **it stays yours**: keep it local, do not redistribute it, and do
not treat the MIT license as covering it.

## Trademark and affiliation

Not affiliated with, endorsed by, or sponsored by The Spooky Team, John White,
or any preset author. "Spooky" is used in the project name as an ordinary
English adjective, not as a product mark. Spooky2 is a trademark of its owner and
is used here only to name the software this tool indexes.

## No medical claims

The vendor's own legal notice is explicit that *"no medical claims are made for,
nor implied by Team Spooky"*, and neither does this project make any. This tool
chooses among programs that already exist. It does not diagnose, and it does not
present the claims of preset authors as medical fact.
