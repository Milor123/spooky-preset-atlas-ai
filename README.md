# Spooky Preset Atlas

<div align="center">
<img width="250" height="250" alt="Ghosty-ty" src="https://github.com/user-attachments/assets/1fe7e77a-4693-4287-b244-4e719a19b8bf" />
</div>

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

These are questions the index genuinely answers. Every one of them is backed by a
count you can check, and none of them asks for more than the tool can deliver.

**"I have a bacterium called *Candida albicans*. What runs for it?"**
669 presets match that name alone. This is the core of what the index is for.

**"I think I have parasites. What should I run?"**
1,280 presets mention parasites. The AI narrows them by your hardware, your
delivery mode and the safety screen, and gives you the exact menu path to load
each one from.

**"I have an XM and no GeneratorX Pro. What can I actually use?"**
Filters to the delivery modes your hardware supports and tells you what to skip.

**"Which Contact presets are safe for a 20-minute session?"**
Applies the Contact rules — 14–20 V against 4–10 V for Remote, 7 minutes on and
21 minutes off — and shows you which ones violate them.

**"What is the difference between these two presets?"**
Full notes, the frequency lines exactly as the file writes them, delivery mode,
the shell it inherits from, and where in the menus each one lives.

**"I think I have something in a specific place. Where do I start?"**
Body sites are indexed too, and small counts are a good sign rather than a bad
one — 243 presets mention *cervical*, 30 mention *cervix*, 18 mention *vagina*.
A small, exact set is more useful than a large vague one.

### The workflow worth knowing

Most people arrive without the technical name. That is normal, and it is where
the assistant earns its keep:

1. **You describe it.** *"Burning when I pee, and an itch."* No Latin, no
   organism name.
2. **The assistant looks it up.** It does not guess. It searches for what the
   symptom pattern points to.
3. **It brings the name back to the index.** Whatever organism the search turns
   up, that name goes straight into the preset database, and you get the
   hundreds of matching presets with the safety screen already applied.
4. **It tells you where to click.** Every result comes with its full path —
   *"Presets tab > DNA/Bacteria/Remote/…"* — so you are not hunting for it.

The index does step 3. The assistant does steps 1, 2 and 4. Neither is much use
without the other.

### Use a large model

This is not a task for a small or fast model. The assistant has to hold a
concept model of what a preset and a program are, keep safety rules in mind
while reasoning, call the tools, and know enough biology to tell a plausible
organism from a made-up one. A mini or flash model will quietly drop a safety
cap, or invent a frequency that was never in the corpus.

Point it at a strong model and the difference is not subtle.

### Where the help stops

**Choosing between presets that already exist is what this does well.** It does
not help you build your own programs from scratch. Doing that well would need
the vendor's factory program catalog, which this project deliberately does not
ship and which resolves only about 2% of the programs presets actually use. If
you want to assemble programs yourself, this is the wrong tool and we would
rather say so than improvise.

It also cannot resolve most frequencies, and it will not pretend otherwise.
About 82% of the corpus states them as molecular weights or base-pair counts
rather than as Hz. Spooky2 converts those on your machine when the program
loads, and what it produces depends on which generator you have attached, so
there is no table that could stand in for it. Those frequencies are reported
exactly as the preset writes them, and the safety screen tells you which ones
it could actually evaluate.

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

**Or just click it.** No account, no `pip`, no command line:

**[⬇ Download spooky.db directly](https://huggingface.co/datasets/Milor123/spooky-preset-atlas-db/resolve/main/preset-db/build/spooky.db?download=true)**

Then put the file at `preset-db/build/spooky.db` inside the cloned repository and
the tools find it with no further configuration.

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
minutes of rest. Plasma carries a 50% duty-cycle hardware cap. Spooky2's own guide (p140) tells
you to blacklist **1840 Hz** and **1910 Hz** across all generators, describing them as
**"believed to cause malignancy growth"** — the manufacturer's own wording is a stated
belief, not an established finding. The blacklist can only be applied when a program
states them literally in Hz — which is a minority of
the corpus, so most presets cannot be screened against this and are not reported
as clean.

Full set with page citations in `preset-db/docs/KNOWLEDGE.md`.

## License

MIT for the code — see [LICENSE](LICENSE). The compiled data and vendor
documentation are **not** covered; see [NOTICE.md](NOTICE.md) for exactly what is
ours, what is theirs, and what we did.

---

## Agradecimientos

Este proyecto no habría existido sin el grupo de Telegram **Spooky2 Deutsch**, y
principalmente sin dos personas que publicaron sus mediciones y se retractaron
cuando se les mostró que estaban equivocados.

**Johannes D** — profesor de matemática. Debe casi todo lo técnico de aquí: la
explicación de por qué los generadores son ARB con 1.024 muestras, la del divisor *Odd*,
por qué el Tissue Factor es un índice de refracción, y el cálculo del peso molecular a
frecuencia. Detectó y corrigió un error de la base de datos de Spooky2, y se retiró
públicamente su propia explicación cuando Jayce le mostró que no aplicaba.

**Joerg Pohl** — ingeniero de señal. La mitad del material eléctrico de este proyecto es
suyo: por qué el Boost es una suma en serie de las dos salidas, cómo funciona el
biofeedback por dentro, los límites de tensión de cada aparato, y los Drivers
correctos de cada modelo. **Cuando se le refuta algo, retira la afirmación entera**, sin
defensa y sin matiz. Ese rasgo es lo que hace que su material sirva.

**Kimmy 29/11** — administradora y owner del grupo. 2.560 mensajes, y el primero de
todos es el que recibió al grupo. Respondió lo que es del producto y no es técnica —
que es justamente la parte que hace falta para que la técnica sirva.

El export de ese grupo, con sus 2.744 mensajes de Joerg y los miles de turnos de
Johannes D, es la materia prima de `teoria-JD/`. **No se distribuye aquí:** es
material de terceros y la decisión de publicarlo es de quienes lo escribieron. Todo lo
que este repositorio usa de él son hechos técnicos comprobables —cifras, mecanismos,
prohibiciones— que se sostienen con o sin la atribución.
