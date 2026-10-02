# The skill

This is a copy of the Pi skill that lives at `~/.pi/agent/skills/spooky2-presets/SKILL.md`.

The installed copy is the working one. This directory is the source of truth for
GitHub, so the two can be compared after any change:

```bash
diff ~/.pi/agent/skills/spooky2-presets/SKILL.md skills/spooky2-presets/SKILL.md
```

## Install

```bash
mkdir -p ~/.pi/agent/skills/spooky2-presets
cp skills/spooky2-presets/SKILL.md ~/.pi/agent/skills/spooky2-presets/SKILL.md
```

Pi picks it up on the next session. To check it loaded, ask something that
should trigger it, such as *"which Spooky2 preset should I run for a parasite"*.

## What it needs at runtime

The skill is only the decision layer. To actually answer, it must be able to run
the query tool in this repository, so clone the repo and build the database once:

```bash
python preset-db/tools/build_db.py --full
python preset-db/tools/audit.py
```

Queries then cost 3–23 MB of RAM and under a second each. Building costs about
two to four minutes and roughly 3 GB of free RAM, once.

## Editing it

The skill encodes the safety rules and the concept model. Two things to keep in
mind if you change it:

- **A program is not a preset.** A program is a named block of frequencies drawn
  from a database. It cannot be run on its own. Never answer a "what should I
  treat this with" question with a bare program name; answer with a preset.
  If a program has to be mentioned, say what it is and that the user needs a
  Shell (Empty) Preset to load it into.
- **Never soften a safety cap.** The caps in the guide are there because of what
  the caps prevent. If a preset violates one, say so and recommend a different
  preset, not a shorter session.
