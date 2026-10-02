# Feature: Spooky2 Preset Database + Preset Selection Skill

## Goal

Turn the 43,397-file Spooky2 `Preset Collections/` txt corpus into a queryable SQLite
database, then expose it to an LLM through a Pi skill so the LLM answers
"which frequency programs should I run for case X" without reading raw txt and
without burning hundreds of thousands of tokens per question.

## Hard constraint: the corpus is READ-ONLY

`Preset Collections/` must never be written, moved, renamed or reformatted.
All tooling writes only under `preset-db/`.

## Measured baseline (verified by read-only analysis)

| Metric | Value |
|---|---|
| `.txt` files | 43,397 |
| Preset blocks (`"[Preset]"` sections, **quoted**, not bare) | 48,461 |
| Programs (`Loaded_Programs` lines) | 174,623 |
| `Loaded_Frequencies` lines | 174,624 (1:1 with programs) |
| Frequency entries | 3,325,549 |
| Distinct preset keys | 264 (~12 are hot) |
| `Preset_Notes` prose | 23.4 MB (~6M tokens) |
| Author codes (` - XX` filename suffix) | 29 (JW 23,120 / EL 1,264 / DB 645 / BY 162 / JRG 96 / JD 58 / MM 51 / AR 38 / JK 20 / EV 14 / BR 12 / BEM 8 / WD 8 / DI 6 / JE 6 / AW 5 / KB 3 / SH 3 / RB / DG / JF / LW / DW / CK / NS / BW / PM / DH / MA) |
| Shell presets (canonical mode taxonomy) | 67 files in `Shell (Empty) Presets/`: Coil, Contact, Plasma, Remote, Scalar |
| Delivery modes | R, C, L, SS, P, Dual, FB, GX, XM |
| PDFs | 23 (define the vocabulary: `(SS)`, GX, Biofeedback, sweeps, peptides) |

`JW = John White`, confirmed by `JW_Peptides/JW Peptides - John White.pdf`.
All `.txt` files contain at least one `[Preset]` block; 48 files hold >10 presets
(max 222: `Morgellons and Lyme/.../Set 'N Forget 3-Day (R) - BY.txt`).

## Non-goals

- No ML model for parsing. Extraction is deterministic code.
- No generative LLM pass over the corpus (48,461 × ~600 input tokens = ~29M input
  tokens; the notes are formulaic boilerplate, so a rule extractor recovers most of
  the value at zero marginal cost).
- Never invent, interpolate, round, complete or "optimise" a frequency. The
  database is a faithful index, not a recommender of numbers.
- Never rewrite a preset file to "fix" it.

## Architecture

```
43,397 .txt  --[1] parser (0 tokens)-->  SQLite
                                     --[2] rule extraction (0 tokens) -->
                                     --[3] local embedding model (0 tokens, CUDA) -->
                                     --[4] skill --> SQL --> 2-5k tokens per answer
```

Layers 1-3 run once and are cached in the DB. Layer 4 is the only per-query cost.

## Tasks

| # | Task | State |
|---|---|---|
| 1 | SQLite schema: taxonomy, preset, program, frequency, doc, tag, FTS5 | in_progress |
| 2 | Deterministic parser: quoted INI, multi-preset files, 3 frequency notations | pending |
| 3 | Pilot on stratified ~1,500-file sample + audit against source txt | pending |
| 4 | Rule-based metadata extraction: tags, duration, warnings, notes_lead | pending |
| 5 | Full-corpus build (43,397 files) + integrity report | pending |
| 6 | Local embedding model (bge-small, CUDA) for semantic search + dedup clusters | pending |
| 7 | Pi skill that queries the DB instead of reading txt | pending |

## Frequency grammar (bounded, measured)

Three notations, split on the first character of each comma-separated token.
**Semantics of the letter codes below are UNKNOWN. Store them as opaque flags.
Do not invent meaning.**

1. `plain` — `326=180 C10000 W2 F0`, `5604.5-5604.5=180`, `CM1234567`
   - `lhs[=rhs]`, lhs may be `a`, `a-b` (range), or an encoded blob
   - rhs: first token = amplitude, remaining tokens = modifiers
   - Modifier families seen: `C<n>` carrier, `CM<n>`, `W<n>`, `F<n>`
   - 201 distinct shapes
2. `tilde` — `~2389M923.939`, optionally `=1` amplitude suffix
   - dominant shape `~####M###.###` (502,507 of 736k sampled); 48 distinct shapes
   - also `~####BC#######`, `~####BL###`, `~####BLR####`
3. `backtick` — `` `0843BC 0710543 ``
   - 7 distinct letter combos (`BC`, `BL`, `BLR`, ...), **and a token may contain a
     nested backtick** (`BC\`m`) so a naive split on backtick corrupts the token

Total distinct token shapes: 109 (plain+tilde+backtick combined).

## Losslessness requirement

Every frequency row keeps `raw_token` verbatim. Every unparsed or ambiguous shape is
counted and reported, never silently dropped. The build must emit an integrity report
that a human can spot-check against the original txt.

## Safety requirement for the skill

Author notes contain explicit disclaimers (e.g. `JW_Peptides` states an epitope is
"experimentally mapped ... not a demonstrated antiviral"). The DB must mark such text
as an **author claim**, not a clinical indication, and the skill must surface it
verbatim with that label. The skill never alters, completes or derives a frequency.

## Commits

(work-unit commit identity recorded per task as tasks close)

## Notes

- Pilot first (task 3) on a stratified sample before the full build (task 5).
- Layer 6 embeddings are for semantic retrieval and near-duplicate clustering, not
  generation. Known redundancy: `Morgellons and Lyme v3.0` repeats ~75 presets across
  Contact/Laser/Plasma/Remote/Scalar that differ only by shell.