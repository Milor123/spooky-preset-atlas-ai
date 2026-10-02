# The skill

The decision layer. It is a standard **Agent Skills** package, so it drops into
most AI agents that support the format, not just one.

## What this is

`SKILL.md` is a single Markdown file with YAML frontmatter. The format was
developed by Anthropic and released as an open standard, so any agent that
implements it can load this skill unchanged.

Required frontmatter fields are `name` and `description`; both are already
present. Everything after the closing `---` is the instruction body, loaded only
when the agent decides the skill is relevant.

## Install

Pick the row for your agent and copy the skill folder into the path it expects.

| Agent | Path | Scope |
| --- | --- | --- |
| **Pi** | `~/.pi/agent/skills/spooky2-presets/` | all projects |
| **Claude Code** | `~/.claude/skills/spooky2-presets/` | all projects |
| **Claude Code** | `.claude/skills/spooky2-presets/` | this project only |
| **Cursor** | `.cursor/skills/spooky2-presets/` | this project |
| **GitHub Copilot / VS Code** | `.github/skills/spooky2-presets/` | this project |
| **Gemini CLI** | `~/.gemini/skills/spooky2-presets/` | all projects |
| **Goose** | `~/.config/goose/skills/spooky2-presets/` | all projects |
| **OpenCode** | `~/.config/opencode/skills/spooky2-presets/` | all projects |
| **OpenClaw** | `~/.openclaw/skills/spooky2-presets/` | all projects |
| **Mistral Vibe** | `~/.vibe/skills/spooky2-presets/` | all projects |
| **Amp, Codex, Letta, Factory** | follow that agent's documented skills directory | varies |

From a clone of this repository:

```bash
git clone https://github.com/Milor123/spooky-preset-atlas-ai.git
cp -r spooky-preset-atlas-ai/skills/spooky2-presets <the path from the table>
```

Restart the agent afterwards. To check it loaded, ask something that should
trigger it, such as *"which preset should I run for a parasite"*.

### About DeepSeek, Kimi, MiniMax and Hermes

These are **models, not agents**. There is no skills directory to install into,
because a model on its own cannot read files or run commands.

What you actually do is point one of the agents in the table above at one of
those models through its API configuration. The skill is loaded by the agent; the
model is what reasons with it. A few of the agents in the table are routinely
driven by exactly those models, and the skill works the same either way.

## What it needs at runtime

The skill is only the decision layer. To actually answer anything, the agent
needs two things: this repository, and a built database.

```bash
cd spooky-preset-atlas-ai
python preset-db/tools/build_db.py --full
python preset-db/tools/audit.py
```

Point it at your own copy of the presets if it is not where the script expects:

```bash
python preset-db/tools/build_db.py --full --presets "<your path>/Preset Collections"
```

The agent then calls the query tool:

```bash
python preset-db/tools/query.py find "parasite" --limit 5
python preset-db/tools/query.py screen "cancer" --shell Contact --limit 5
```

Queries cost 3–23 MB of RAM and under a second each. Building costs two to four
minutes and roughly 3 GB of free RAM, once. Only the standard library is
required — no `pip install`.

**A prebuilt database is published on Hugging Face** for anyone who would rather
download than build:

```bash
pip install huggingface_hub
hf download Milor123/spooky-preset-atlas-db preset-db/build/spooky.db \
  --repo-type dataset --local-dir .
```

**[huggingface.co/datasets/Milor123/spooky-preset-atlas-db](https://huggingface.co/datasets/Milor123/spooky-preset-atlas-db)** — 1.09 GB, one file, the complete index with FTS5 search.

An index built from your own licensed copy contains your vendor's content, so
**it stays yours**. Download it and use it; do not pass it on. Building your own
instead costs two minutes and removes the question entirely.

## Agents that cannot run scripts

Claude.ai and similar chat-only clients can load the skill as uploaded
instructions, but they have no shell. They will get the safety rules, the
concept model and the reasoning, and **will not** be able to query the database.
For those, the value is the guidance, not the search.

## Editing it

Two things to keep in mind if you change it:

- **A program is not a preset.** A program is a named block of frequencies drawn
  from a database. It cannot be run on its own. Never answer a "what should I
  treat this with" question with a bare program name; answer with a preset. If a
  program has to be mentioned, say what it is and that the user needs a Shell
  (Empty) Preset to load it into.
- **Never soften a safety cap.** The caps in the guide are there because of what
  the caps prevent. If a preset violates one, say so and recommend a different
  preset, not a shorter session.

Agents that read the standard will pick up new frontmatter fields without
complaint, so adding `license`, `metadata` or `allowed-tools` is safe. Keep `name`
matching the directory name.
