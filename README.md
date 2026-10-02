# Spooky Preset Atlas

**You have 48,463 Spooky2 presets. This lets you ask an AI which one to run — in plain language, without reading a single file.**

Remote, Contact, Plasma, Scalar, Coil and Cold Laser. Bacteria, viruses,
parasites, fungi, detox protocols, cancer collections, biofeedback, frequency
sweeps. The AI searches them, applies the safety rules, and tells you what to do.

> **Not affiliated with, endorsed by, or sponsored by The Spooky Team or any
> other preset vendor.** "Spooky" here is an ordinary English adjective, not a
> product mark. This repository ships no presets, no notes and no vendor
> documentation. You build the index from your own licensed copy of Spooky2.

---

## The short version: hand the link to your AI

Open this URL and give it to whichever AI you use:

```
https://github.com/Milor123/spooky-preset-atlas-ai
```

Then say something like:

> *Install the skill from this repository and get it working. I have Spooky2
> installed at (your path). I don't want to run any commands myself — tell me
> what to do if you need me to do something.*

The AI will clone the repository, install the skill where your agent expects it,
build the index from your own copy of Spooky2, verify it, and then start
answering questions. It knows the format and the paths.

**You do not need to know how to code, run a terminal, or read a config file.**
The only thing you need is a licensed copy of Spooky2 already on your machine.

---

## What you can ask

Once it's set up, this is what the conversation looks like. These are questions
the index genuinely answers, and the limits are stated rather than glossed.

**"I think I have a parasite infection. What should I run?"**
Searches every preset that mentions parasites across 4,192,779 frequency lines,
and returns the candidates with the safety screen already applied.

**"I want to do a detox. Sequence me a protocol."**
Pulls the kill / heal / detox chains in order, respecting the vendor's timing
rules about what must not run on the same day.

**"I have an XM and no GeneratorX Pro. What can I actually use?"**
Filters to the delivery modes your hardware supports, and tells you what to skip.

**"Which presets use Contact mode, and which ones are unsafe for a 20-minute session?"**
Applies the Contact rules — 14–20 V against 4–10 V for Remote, 7 minutes on and
21 minutes off — and shows you which presets violate them.

**"Which of these should I try if nothing happens in three days?"**
The vendor's own rule is to switch to a different program rather than push on.
The AI applies it.

**"What's the difference between this preset and that one?"**
Full notes, frequency list, delivery mode, and the base preset it inherits from.

**"Find me presets that don't use 1840 Hz."**
It will find the 23 presets that use it literally — and it will also tell you it
can see 2,547,746 frequency references whose value it cannot compute, so it
cannot rule out that frequency arriving through one of those. That answer is
more useful than a clean number would be.

### Where the help stops

**Choosing between presets that already exist is what this does well.** It does
not help you build your own programs from scratch. Doing that well would need
the vendor's factory program catalog, which this project deliberately does not
ship and which resolves only about 2% of the programs presets actually use. If
you want to assemble programs yourself, this is the wrong tool and we would
rather say so than improvise.

It also cannot compute most frequencies. The corpus stores about 81% of them in
a private notation — molecular weights, base-pair counts — and the conversion
arithmetic is not documented anywhere we can find. Those frequencies are
reported as unresolved, never guessed.

**"I have a Shell (Empty) Preset and want to build my own program. Where do I start?"**
Explains the difference between a preset, a program and a shell, and walks you
through loading programs one at a time.

The AI brings the medical and biological reasoning. This index brings the facts
it would otherwise have to guess at.

---

## What you need

| | |
| --- | --- |
| **A licensed copy of Spooky2** | Required. The index is built from your own `Preset Collections` folder. |
| **Python 3.9 or newer** | Already installed? Nothing to do. No `pip install`, no packages. |
| **~3 GB of free RAM, for 2–4 minutes** | Only to build the index. After that, queries use 3–23 MB and take under a second. |
| **An AI agent that supports skills** | Claude Code, Codex, Cursor, Copilot, Gemini CLI, Goose, OpenCode, Pi, and others. See [the skill README](skills/spooky2-presets/README.md) for the full list and paths. |

Nothing is uploaded anywhere. The index is built on your machine and stays there.

---

## If you'd rather do it yourself

```bash
git clone https://github.com/Milor123/spooky-preset-atlas-ai.git
cd spooky-preset-atlas-ai

# point this at your own copy if it is not in the default place
python preset-db/tools/build_db.py --full --presets "S:\Spooky2\Preset Collections"
python preset-db/tools/audit.py
```

Then install the skill into your agent, and ask it questions:

```bash
python preset-db/tools/query.py find "parasite" --limit 5
python preset-db/tools/query.py screen "cancer" --shell Contact --limit 5
```

`screen` applies the mechanical safety rules in a single call, which is what the
skill uses before it recommends anything.

---

## A prebuilt index, if you'd rather not build one

Download it instead of spending two minutes building:

```bash
pip install huggingface_hub
hf download Milor123/spooky-preset-atlas-db preset-db/build/spooky.db \
  --repo-type dataset --local-dir .
```

**[huggingface.co/datasets/Milor123/spooky-preset-atlas-db](https://huggingface.co/datasets/Milor123/spooky-preset-atlas-db)** — 1.09 GB, one file.

It is the full index: 48,463 presets, 174,624 programs, 4,192,779 frequency
lines, FTS5 search included. Drop it at `preset-db/build/spooky.db` and the tools
find it with no further configuration.

To publish an index you built yourself, `preset-db/tools/publish_db.py` does it
in one call.

**Note on this one.** The index contains the vendor's and the preset authors'
content — preset names, their descriptions, their frequency lines — restructured.
That content is **not** covered by the MIT license, and it stays yours to use
locally. Do not pass the database on. If you would rather not take that on, build
your own from your own licensed copy; it takes two minutes and the result is
unambiguously yours.

---

## What this is not

- **It does not diagnose anything.** It helps you choose among programs that
  already exist. That is a different thing from telling you what you have.
- **It does not vouch for the presets.** The authors of these programs make
  claims this project neither repeats nor endorses. The vendor's own legal
  notice says no medical claims are made for, nor implied by, Team Spooky.
- **It will not soften a safety rule.** If a preset violates a cap, the answer is
  a different preset, not a shorter session.

**Consult your doctor before using Spooky2, and do not use it to treat a
condition instead of being seen.**

---

## What's in the repository

```
skills/spooky2-presets/SKILL.md  the skill — see its README to install
preset-db/schema/                 database schema
preset-db/tools/                  build, query, audit, rebuild
preset-db/docs/KNOWLEDGE.md      our notes on the User's Guide, cited by page
```

The index itself, the preset corpus and the User's Guide are **not** here. This
is the engine, and you run it on your own copy.

**Your `Preset Collections` folder is read-only and always will be.** Nothing in
this repository writes to it, moves it, renames it or reformats it. Every tool
here writes only under `preset-db/`. If you fork this and add an indexer, keep it
that way.

## Safety rules the skill enforces

Contact delivery runs at 14–20 V against 4–10 V for Remote, and is the
highest-power mode available. Contact zapping is capped at 7 minutes with 21
minutes of rest. Plasma carries a 50% duty-cycle hardware cap. **1840 Hz** (83
occurrences across 22 presets) and **1910 Hz** are treated as blacklisted.

Full set with page citations in `preset-db/docs/KNOWLEDGE.md`.

## License

MIT for the code — see [LICENSE](LICENSE). The compiled data and vendor
documentation are **not** covered; see [NOTICE.md](NOTICE.md) for exactly what is
ours, what is theirs, and what we did.
