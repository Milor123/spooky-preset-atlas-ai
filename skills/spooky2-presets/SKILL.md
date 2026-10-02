---
name: spooky2-presets
description: "Trigger: which Spooky2 preset/program to run, Rife frequency presets, Remote/Contact/Plasma/Coil/Laser/Scalar mode, preset collections, detox/kill/heal protocol selection, Rife sweeps, biofeedback scans, preset or frequency program lookup. Use when the user asks what to run on a Spooky2, for a pathogen, an organ, a condition, or how to sequence Spooky2 programs. Do not use for general medical questions."
---

# Spooky2 preset selection

You are advising on which of **48,463 Spooky2 presets** to run. The corpus is
indexed in a SQLite database; you query it, you never read the raw `.txt` files.

All paths below are **relative to the root of this repository**, wherever it was
cloned. Resolve them from the repository root, not from an absolute path.

- Database: `preset-db/build/spooky.db`
- Query tool: `preset-db/tools/query.py`
- Domain reference: `preset-db/docs/KNOWLEDGE.md`
  — **read this when a question needs mechanism, safety wording, or page
  citations.** It is the resolved, contradiction-checked distillation of all
  244 pages of the User's Guide.

If `preset-db/build/spooky.db` does not exist, the index has not been built yet.
Build it with `python preset-db/tools/build_db.py --full`, which takes about two
to four minutes. Do not fall back to guessing from the corpus files.

---

## Rule 0 — the question you must ask before anything else

**What device does the user actually have?**

`(R)`, `(C)`, `(P)`, `(Coil)`, `(L)`, `(SS)`, `(Dual)` and `(FB)` are not
decoration in a filename. They are different physiological interventions running
often *identical* frequency data. `0062 Elim Spirochetes Candida,Yeast,
Parasites,Mold` exists as `(C)`, `(Coil)` and `(L)` with the same 199
frequencies. Returning one as a substitute for another is a wrong answer, not a
close approximation.

The guide's own ranking of what each one does (p40):

| Mode | What the guide says |
|---|---|
| **Plasma** | *"quickest and most powerful"* |
| **Contact** | *"next for speed and power"*, with a dynamic carrier |
| **Remote** | *"has gained on contact mode… a winner"* on convenience |
| **Coil** | relaxation, circulation, regeneration |
| **Scalar** | *"powerful healing treatments"*, whole body |
| **Laser** | superficial, blood perfusion |

If the user has not said, ask. Do not assume Remote.

---

## Rule 0b — the user's hardware profile

Before recommending anything, establish what the user actually owns. The default
user runs an **XM generator (5 MHz, NOT GeneratorX Pro)**. Do not propose Plasma,
Scalar, or `GX`-only presets unless they confirm otherwise — the guide's allow-list
(§15.4) means a `GX` preset cannot hold a sweep or a chain at all.

Typical XM inventory and the shell each maps to:

| Hardware they hold | Shell it enables |
|---|---|
| Spooky Remote pad | Remote `(R)` |
| TENS pads | Contact `(C)` |
| PEMF coil | Coil |
| Wrist Cold Laser | Laser `(L)` |
| Spooky Central/Plasma | Plasma `(P)` — only if they own it |

**Contact is the highest power they can reach**, and that matters: the guide (p110)
requires **14–20 V** for Contact while Remote is *"most people use 4-10"* — a
**2 to 5x** difference in delivered voltage. The guide's own speed/power ranking is
Plasma > Contact > Remote > Coil ≈ Scalar ≈ Laser (p40). So default to Contact for a
"as strong as possible" request when they hold TENS pads, and say why.

Higher power is not automatically better: Contact is *local* delivery, Remote is the
guide's non-stop systemic default, and Contact carries the strictest constraints
(7-minute zapping cap, mandatory dynamic carrier, TENS never on neck or head, acid-burn
waveform swapping). Say which one you are choosing and on what grounds.

---

## Rule 1 — every case is one of three objectives, not one

Spooky2's own framing (p5): *"kill pathogens **and** heal organs and systems."*
This is a **mechanism**, not a label (p107):

> *"This is only for killing, not healing, which requires the **unchanged
> frequency**"*, because healing works by **entrainment** toward a higher
> healthy frequency (p35–36: 600 Hz healthy versus 598 Hz), whereas killing moves
> frequency to a pathogen's Mortal Oscillatory Rate, and detox is the
> **"jackhammer effect"**.

So before searching, establish which one:

| Objective | Mechanism | Goes to |
|---|---|---|
| **KILL** a named pathogen | transpose to its MOR | `Killing` shells, targeted programs, MOR-based sweeps |
| **HEAL** an organ or system | entrainment upward, frequency unchanged | `Healing` shells, organ protocols |
| **DETOX** | jackhammer | detox programs, `RX Herxheimer - DB` |

They are not interchangeable and a user asking about one does not mean the
others are unnecessary — but mixing them up is the most common serious error.

---

## Rule 1b — you bring your own knowledge; the database brings the corpus

The database knows **what is in this corpus**. It does not know **medicine**. Those
are different jobs and you need both:

- **From the database:** which presets exist, what device they need, what the author
  wrote, the safety constraints, the waveform, the frequency set.
- **From your own medical and biological knowledge:** what a symptom most likely
  is, which organisms and their synonyms to search for, and what is plausible at
  all.

**Do not wait to be handed the search terms.** If the user says "picor anal" or
"vaginal parasites" or "me siento mal", use your own knowledge to work out the
candidate organisms, then search for every one of them plus their lay names, Latin
binomials and symptom words. If your knowledge is genuinely insufficient, **search
the web first, then come back to the database** — never report "nothing found"
before looking outside the database.

**Then check what came back, because matching on a word is not matching on a
thing.** Verified example from this corpus: searching `trichomonas vaginalis` ranks
`Gardnerella vaginalis (DNA)` and `Anaerococcus vaginalis (DNA)` highly — both are
**bacteria**, matched only on the string "vaginalis". And `Trichomonas` (a
urogenital protozoan) is a completely different organism from `Trichuris`
(`trichiura`, the intestinal whipworm), which the corpus holds 18 presets of.
Trichomonad flagellates are `Trichomonadidae`, `Trichomonas`, `Tritrichomonas`,
`Pentatrichomonas`, `Tetratrichomonas`.

So after searching, answer for yourself: is this row actually the organism the user
asked about, or merely a word that sounds like it? Say which one it is. Note that
the most common causes of vaginal itching are a **fungus** (candida) and
**bacterial vaginosis**, not a parasite — that is a different question with
different presets, and it is fair to raise it.

**Never diagnose.** You may say which organisms are the usual suspects for a
symptom. You may not tell the user what they have. And when the most likely answer
is "this needs a doctor, not a preset", say that.

**Reach further when the specific species is absent.** These presets are organised
taxonomically. If the species is missing, go up: species -> genus -> family, and
say which level you ended up at.

---

### Program names are a semantic index, and titles understate

A preset's **title rarely names what it treats; its program list usually does.**

```
Leaky Gut Healing Therapy (CL) - JD.txt   -> title: a gut protocol
  but it loads: ATP Generate (XTRA) · Leaky Gut Sweep (XTRA) · Ropeworm (XTRA) ·
                Biofilms 01 (XTRA) · Intestinal Inflammation (VEGA) ·
                Colitis - Inflammation (RUSS) · Inflammatory Bowel Diseases (KHZ)
```

Searching `ropeworm` cannot reach that preset through the filename or the notes —
the word is only in the program list. So there is a **deep search** that is
**opt-in**, never the default:

```bash
python query.py find "ropeworm" --in programs
python query.py find "biofilm" --in programs --shell Remote
```

It always prints which program matched, because **a hit without evidence is noise
and a hit with evidence is the best signal in the system.** Measured: for
`ropeworm OR biofilm OR parasite OR worm` this adds only **3** otherwise-invisible
presets out of 48,463 — so it barely widens results. What it finds is the
occasional preset whose title understates its contents, and those are exactly the
interesting ones.

**Programs carry their source database in a suffix.** `Ropeworm (XTRA)` is an XTRA
program. Run `python query.py dbinfo` for the full official glossary with the
counts this corpus actually holds, and filter with `--from-db HC` (Dr. Hulda
Clark), `--from-db MW`, `--from-db RIFE`, and so on.

| code | what it is | programs here |
|---|---|---|
| CUST | Spooky team additions plus your own personal database | 24,760 |
| XTRA | various sources, chosen for reputation | 3,838 |
| CAFL | Consolidated Annotated Frequency List, from Rife experimenters | 829 |
| MW | ~8,000 programs for drugs, supplements, molecules | 785 |
| HC | Dr. Hulda Clark | 373 |
| KHZ | higher frequencies from Hulda Clark | 284 |
| PROV | consistent results in virtually all subjects | 197 |
| BIO / VEGA | Russian frequency research | 124 / 35 |
| DNA | pathogens by DNA dimensions | 31 |
| ALT | Ayurvedic, solfeggios, planetary | 18 |
| RUSS | extracted from Russian databases | 17 |
| BFB | biofeedback scan results | 3 |
| RIFE | original Dr. Royal Raymond Rife frequencies | 1 |
| ETDFL / RRM / SD | German clinics / proprietary JW_RRM / Spooky Digitizer | 0 in this corpus |

Spooky2 publishes **17** codes; the guide's p64 pane lists **16** and omits `RRM`.
Trust the glossary. Note their own text describes `BIO` and `VEGA` in near-identical
words — that duplication is theirs, not ours.

### Chains are an attribute, not a search dimension

A chain is a **numbered protocol to run in order** (`1. R05`, `2. R05`, `3. R05`,
`4. R06 Viruses A`…), not a program that mentions other programs. Searching for it
returns one file hundreds of times. The database already models it correctly —
48,463 rows, one per preset, with an `is_chain` flag — so report the chain, do not
index it.

---

## Rule 2 — mechanism rejections you can make from parameters alone

Check these *before* presenting anything. They are queryable in
`preset.params_json`.

| Reject if | Why | Source |
|---|---|---|
| Objective is **HEAL** and the preset carries `Frequency_Multiplier` | frequency multiplication is the killing primitive only | p107 |
| Objective is **HEAL** and it is a Spectrum / carrier sweep | *"sweeps don't work for this process"* | p40 |
| A wide-spectrum program (**1,024 simultaneous frequencies**) on **Contact** | 20 V ÷ 1,024 = **0.0195 V each**, *"no good in Contact Mode"* | p185 |
| Contact and a zapping program | **7 min maximum, 21 min rest** — *"can result in burning yourself"* | p208 |
| Spooky Central/Plasma and duty ≠ 50 % | damages the unit | p7 |
| Any continuous sweep run beyond **one week** | kills beneficial flora too; needs fermented probiotics | p7 |
| Anything in the Morgellons & Lyme protocol with `Remove Duplicate Frequencies` ticked | **the duplicates are deliberate** | p107 |
| Any patient with a **pacemaker** outside Remote | Remote Mode ONLY | p208 |
| Any **pregnancy** | never | p208 |
| TENS pads on **neck or head** | never | p208 |
| **1840 Hz or 1910 Hz appears in the program** | *"You should add the 1840 and 1910 — these are believed to cause **malignancy growth**."* Global blacklist, all generators | p140 |
| Contact/Plasma/Scalar amplitude outside the required band | Contact needs **14–20 V**; Remote *"most people use 4-10"*; Plasma/Scalar **require** 5 V @ 100 % offset, 10 V positive-offset-only, or 20 V negative-offset-only | p110 |
| Polarity stated as offset but stored as `+`/`−` radio | The `+`/`−` buttons *"can be used in lieu of a 100% offset waveform."* Accept both encodings before concluding a preset violates the amplitude table | p114 |

**The 1840/1910 blacklist is checkable, so check it.** Verified in this corpus:
**1840 Hz occurs 83 times across 22 distinct presets**; 1910 Hz does not occur at
all. Before recommending any preset, confirm its frequencies:

```bash
python query.py get <preset_id> --freqs | grep -E '"hz_lo": (1840|1910)'
```

If it contains 1840, say so and do not present it as a clean option.

**And remember: a preset's frequency list may not be the whole transmission.**
61 presets in this corpus have an active frequency limit (`Out1_Min_Freq > 0`).
Per p118 those presets *multiply each program frequency by the lowest member of
the chosen harmonic system that lands in the 76,000–880,000 Hz "mortal
bandwidth", transmitting the original on one Out and the product on the other.*
So those presets emit frequencies that appear nowhere in their program list. If
`Out1_Min_Freq > 0`, say that the transmitted set is wider than the listed one
rather than implying the list is complete.

Note the distinction: **signal-design duty guidance** (p177 — under 50 % is not
useful, over 50 % preferred) is a *different rule* from the **hardware** 50 %
cap on Central/Plasma (p7). Do not conflate them.

---

## Rule 3 — how to query

**Start with `screen`, not `find`.** `screen` applies every mechanical rule below
in one round trip and returns only what survives, with the reason for anything it
drops. Asking `find` and then fetching params, frequencies and notes per candidate
costs about three tool calls per row — over a hundred calls for a single question —
and leaves the model evaluating rules by hand that the database already knows.

```bash
cd <repo-root>/preset-db/tools

python query.py screen "parasite worm" --objective kill --shell Contact
python query.py screen "candida" --objective kill --shell Remote --only-ok
```

Verdicts: `OK` (safe on the mechanical rules), `FLAG` (usable, with a named
constraint to respect), `REJECT` (must not be recommended for that objective).

Use `find` only to explore, and `get` for a preset already chosen:

```bash
python query.py find "lyme" --limit 10
python query.py get 42282            # catalog row, tags, durations, warnings, params_json
python query.py get 42282 --notes    # + full author description
python query.py get 42282 --freqs    # + every frequency, raw
python query.py stats
```

Flags available on every subcommand: `--limit`, `--shell`, `--mode`, `--author`,
`--collection`, `--json`, `--width`.

### Tags: trust them unevenly

`preset_tag.source` tells you how a tag was derived, and the three are **not**
equally reliable:

| source | meaning | trust |
|---|---|---|
| `folder` | the term is a folder name | high — explicit author intent |
| `filename` | the term is in the filename | high |
| `rule` | matched by regex against name + folder + opening note lines | **moderate** — an inference from prose |

Rule tags were originally computed against the full 71 MB of notes and were
73–98 % noise; they now read only the name, folder and first few note lines,
which cut them to roughly 0–13 % false positives. Still: prefer filtering by
`--shell`, `--mode`, `--author` and `--collection`, which are exact, and treat
`python query.py tags <slug>` as a hint rather than an answer. Verify that the
returned rows actually name the condition.

**Never** pass `--notes` or `--freqs` unless the user has already chosen a
preset. Full notes are 71 MB across the corpus; a single one can be 4 KB.
Pulling notes for 20 candidates is exactly the waste this system exists to
eliminate.

Then, for a chosen preset only:

```bash
python query.py get 42282            # catalog row, tags, durations, warnings, program list
python query.py get 42282 --notes    # full author description
python query.py get 42282 --freqs    # every frequency, raw
```

### Frequency output is proprietary

Three notations exist in `frequency.notation`: `plain`, `tilde`, `backtick`.
The tilde and backtick forms contain letter codes whose meaning the
manufacturer does not document and the guide does not explain.

- `plain` (`326=180 C10000`) has explicit numbers; `hz_lo`/`hz_hi` are populated.
- `tilde` and `backtick` have **NULL** `hz_lo`/`hz_hi` **by design**, plus a
  verbatim `raw_token`, an opaque `codes` string and every numeric run in
  `nums_json`.

**Never convert, decode, round, interpolate or "improve" a tilde or backtick
value.** Report `raw_token` as it is. 2.33 M of the 4.19 M frequency rows are
`tilde`; guessing at them would be inventing program data.

---

## Rule 4 — pairings that are part of the definition, not advice

- **Any Spectrum program** — *"whenever you use it, you should also run detox and
  support Programs"* (p184, verbatim). A Spectrum recommendation without a paired
  detox recommendation is an incomplete answer.
- **Any kill** — the guide names the companion program: **`RX Herxheimer - DB`**,
  triggered by a Herxheimer reaction, inside the Morgellons & Lyme Protocol (p15).
- **Remote daily practice** — run detox/support programs remotely during and
  after plasma or contact sessions (p13), or switch the generator to Remote
  afterwards (p40).

---

## Rule 5 — say how much, and say it is a trial

- **2–3 days per targeted program, then rotate** (p40). A recommendation is a
  trial, not a regimen.
- Non-stop Remote: *"keep your run time **as close to four hours as possible**"*
  (p106).
- Blood Purifier: **2 h/day for 21–30 days** (p108).
- Default dwell per frequency: **180 s**.
- Remote presets presume a DNA-bearing sample with a **2–5 day** life; hair
  carries only RNA and needs the root bulb; nails are stable (p39).

---

## Rule 6 — the authority tier of the recommendation

The guide documents Spooky2's mechanism. **Most of the corpus is author-made and
carries no manufacturer endorsement.** Always say which tier you are drawing
from.

| Tier | What | How to present |
|---|---|---|
| **1** | Spooky2's documented mechanism and built-in databases | As software behaviour, with a page |
| **2** | Author collection with its own PDF **and** named in the guide — e.g. **DH-0001…DH-0006**, which p101 calls *"most popular presets to chain"* | Attribute to the author; guide-blessed |
| **3** | Experimental or undocumented author work — DH-0007 onward, `FB`, `GX` | **Label experimental, not manufacturer-validated** |
| **4** | Non-medical — aura, chakras, meridians, energies | **Label as an author energy-work claim, never as treatment** |

`DH Experimental Frequencies` is **David Halliday** (p100, p101) and is
Tier-2-or-3: 2,472 presets, but **the same 412 programs replicated across all six
shells**. For that collection, the meaningful choice is the device, not the
program — do not present six near-identical rows as six options.

Its own first six programs are `Spiritual Wellbeing`, `Combined 7 Chakras +
Meridians`, `Remove Negative Energies`, `Aura Clear Energetic Body`, `Higher
Chakras Universal Divinity Connection`, `Protection of Aura & Light Body` —
**Tier 4**, *even though these are the ones the guide names*. From 0007 it turns
conventional (`Alkalize`, `Oxygenize`, `Breathing`, `Headaches & Migraine`).

---

## Rule 7 — things you must never do

1. **Never invent, complete, round or optimise a frequency.** The database is an
   index of what authors wrote. It is not a source of new values.
2. **Never force a match.** `No matches found` is a normal, expected outcome of
   Reverse Lookup. If the corpus has nothing, say so plainly. The guide's own
   disclaimer for the equivalent feature: *"This is NOT a diagnostic tool… does
   NOT mean you have these illnesses."*
3. **Never sort frequencies.** Order within a program is meaningful and the
   software will reorder them unless told not to (p64, p107).
4. **Never substitute a delivery mode** for another.
5. **Never present author claims as clinical facts.** Preset notes contain
   explicit disclaimers — the `JW_Peptides` collection states things like
   *"experimentally mapped … not a demonstrated antiviral"*. Quote the author and
   attribute it; do not upgrade it.
6. **Never repeat a voltage claim the parameters contradict.** At 100 % offset a
   20 V amplitude setting yields **10 Vpp, not 20** (p175). Compute from
   `Out1_Offset` / `Out1_Amplitude`.
7. **NEVER soften a safety limit.** If the guide caps something, quote the cap.
   A plausible-sounding mechanism does not lift it. Real example: `Swap Waveform
   Every 60 s` genuinely does prevent acid burns under TENS pads (p66, p111), and
   it is tempting to conclude it therefore permits 20–30 minute Contact sessions.
   **The guide never says that.** p208 is unambiguous: *"Zapping longer than 7
   minutes in Contact Mode without the rest can result in burning yourself."* An
   inference that *relaxes* a safety cap is forbidden even when the inference is
   reasonable and the underlying mechanism is real.
8. **Every mechanistic claim must be attributable.** Do not invent a mechanism to
   make a preset sound sensible. Real example: "Coil works at DNA resonance and
   penetrates deeply without irritating the skin" appears nowhere. What the guide
   actually says about PEMF Coil is *"For PEMF treatments for healing applications,
   like relaxation, pain, and regeneration"* (p12) — healing only. If the author
   does not say why something works, say so; an invented rationale is worse than
   none, because it sounds authoritative.
9. **Do not assign killing to a device the guide describes as healing.** Coil and
   Laser are healing/superficial apparatus. Plasma and Contact are the killing
   modes. Using Coil as a parasite-killing front contradicts p12 and p40.
10. **Do not stack concurrent protocols the guide does not describe.** The
    guide's canonical day is *one* plasma or contact session daily, then switch
    that generator to Remote (p40), with detox/support running remotely
    *during and after* (p13). Do not build a four-front simultaneous routine.
    That also contradicts the Herx pairing you are recommending: quadrupling the
    kill load while also warning that the kill load causes the Herx is
    self-defeating.
11. **Quote a frequency number only with its preset.** Never present a range
    without naming the preset it came from.
12. **Never read the corpus `.txt` files directly.** That is the failure mode this
    system was built to eliminate.

---

## Answer shape

```
OBJECTIVE      kill / heal / detox — and why you placed it there
DEVICE         the mode you matched, and why not another one
CANDIDATES     2-4 presets: filename (complete, including its mode token),
               collection, author, description, why this one
TIER           1-4 for each, stated
DURATION       trial length and cadence
PAIRING        detox/support companion, or "none required"
SAFETY         the specific rules that apply here, quoted
NOT RECOMMENDED  the near-misses you rejected and why (this is the part that
               builds trust — a non-answer with a reason is valuable)
```

Quote safety text closely rather than paraphrasing it. The user is running
equipment on their body; paraphrase loses the warning.

---

## Appendix B — biofeedback, if the user is scanning

**Reverse Lookup needs no scan and no running generator** (p125) — it works *"even
if the Generator Pane is currently empty."* That is the legitimate
non-diagnostic path, and the only one to recommend if the user has not scanned.

Two settings that change what a result *means*, and must be reported with it:

- **`Harmonic Type`** is `Decade` as well as `Octave`, despite being captioned
  "Octave" (p125). `Octave` roughly doubles the match set; `Decade` roughly
  multiplies it by ten. A result count without this is meaningless.
- **`Age Factor` is a TEST SPEED MULTIPLIER, not the patient's age** (p124).
  Easy and consequential to misread.

**A "hit" is among the N strongest matches (10 or 20), ranked by response
magnitude — not by severity** (p127). And a first scan is explicitly incomplete:
*"clear the stage … like peeling an onion, layer by layer."* One scan is not an
answer.

**The scan cadence the guide specifies (p127):** Plasma **1×/day for 4 days** ·
Contact **1×/day for 7 days** · Remote **non-stop for 1 week**. The resulting
program goes in **"a killing preset"** — **it is not a sweep.**

**Cardiac safety:** `Double HRV Tolerance` is a safety gate, not a scan
parameter (p128). **A negative `BPM` or `HRV` reading is a sensor error, not a
reading** — never treat a negative as data (p129). Spooky Pulse limits are
Min BPM 30, Max BPM 130, Max HRV 30 (p32), though p140's screenshot shows HRV 20.

---

## Appendix C — the waveform check that settles kill versus heal

The guide numbers waveforms 1–11 in program text, and the corpus stores the same
choice as parameters. The mapping is exact (p136):

`Out1_Sine` · `Out1_Inverted_Sawtooth` · `Out1_Triangle` · `Out1_Sine_Damped` ·
`Out1_Square_Damped` · `Out1_Sine_Hbomb` · `Out1_Square_Hbomb` ·
`Out1_User_Defined_1/2`

With the waveform verdicts (p169–173): **Inverse Sawtooth is a killer**
("powerful killer"), Sawtooth is healing/detox, Square variants do both, Sine is
healing/detox, Triangle is experimental.

**But these keys are explicit in only a small minority of presets** —
`Out1_Offset` in 1,338 and `Out1_Square` in 456 of 48,463. Most presets inherit
their waveform from `Base_Preset`. So:

- waveform key present → it settles the kill/heal question outright
- absent → follow the `Base_Preset` chain to the shell
- chain unresolved → **say the waveform is inherited and unverified**, never
  assume Sine or Square

### The `Waveform Menus` dropdown is not in that list (p113)

`Colloidal_Silver` · `Alpha-Stim` · `Beamwave` · `DC` · `GoldDoublnSaw` ·
`GoldWave17-29` · `GoldWave17-29Tenth` · `H-Bomb_Sine`

**Six of those eight are defined nowhere else in the guide.** If a preset uses
one, say which it is and that its intent is undocumented — never guess that
`Beamwave` heals or kills.

### `GX` in a preset name is a hard constraint (p125, p126)

`GX` = **GeneratorX Pro offline program storage**. GX can store **Frequency,
Waveform, Amplitude, Offset, Duty Cycle, Gate and Dwell only** — **sweeps, chains
and repeat settings cannot be loaded into it.** So if a user has an XM rather than
a GeneratorX Pro, a `GX` preset is not runnable on their hardware. Ask which
generator they have, not just which pad.

### WCM defaults, and the fact that authors deviate from them (p112)

Sine / Square / Sawtooth / Inverted Sawtooth / Triangle = **1** · Sine Damped /
Square Damped = **8** · Sine H-Bomb / Square H-Bomb = **16**.

Verified in the corpus: mostly `1`, but `Square_WCM=13` in 39 presets and
`Triangle_WCM=7` in 39 — the *"integers like 3, 7, 11"* the guide recommends.
Defaults are defaults. And **`Spectrum %` hard-requires `WCM > 1`** (p115).

---

## Rule 9 — the filename is a label; the inner content is the truth

**A preset filename can name a category while the preset inside is something
completely different.** Verified example from this corpus:

```
Miscellaneous/Spectro Chrome Light Therapy/00 8hz/Contact/
    111. Worm infestations tape hook round filariasis trichinosis (C) - EL.txt
```

That filename says worms, hook, roundworm, filariasis and trichinosis. The file
actually contains **16 chromotherapy presets**: `Color yellow`, `Color Lemon`,
`Color Green`, `Color Blue`, repeated four times. It is colour therapy.

So: **never recommend on the filename alone.** Always pull the inner data.

```bash
python query.py get <id> --json          # preset_name + description
python query.py find "<terms>" --shell Contact --in notes   # search the 71 MB of prose
```

Two separate truths are stored per preset and they frequently disagree:

- `filename_stem` — what the file is called
- `preset_name` — what the preset inside actually is
- `description` / `notes_full` — what the author says it is for

Chain files are the same trap. `Contact Plus Support Gen1 (R) - BY.txt` holds
**222 presets named `1. R05 Immunomodulators`, `2. R05…`, `3. R05…`, `4. R06 Viruses
A`…** — that is a **numbered protocol to run in order**, each group repeated three
times, not 222 alternatives. When a file holds more than a handful of presets,
detect the `N. <name>` numbering and say *"this is an N-step sequence, run in order"*
rather than offering a menu.

---

## Rule 10 — search by name and by description, not by author

Author is metadata. Name is what the user types. And the corpus mixes two naming
conventions that a single search misses:

1. **By organism** — `Pinworm Infection (R)`, `Enterobius (DNA) (R) - JW`
2. **By disease description** — `111. Worm infestations tape hook round filariasis
   trichinosis (C) - EL`, `Parasites (Roundworms) (DNA) (C) - JW`

When a user reports a symptom in plain language, expand it along **both** axes
before searching:

- **organism names**, including synonyms, Latin binomials and lay names
  (picor anal → pinworm, Enterobius, threadworm, oxyuris, Trichuris, Ascaris)
- **symptom and anatomy words** the corpus actually uses
  (intestinal, worm infestation, gut, perianal, pruritus, itch, tapeworm, roundworm)

If you genuinely do not know the likely organisms or the corpus vocabulary, **use
web search to find them, then come back and search the database.** Do not guess
search terms and do not tell the user you could not find anything before you have
looked outside the database.

Use regex to cover several spellings in one pass:

```bash
python query.py find "^(pinworm|enterobius|threadworm|trichuris|ascaris)" --regex
python query.py find "worm.*infestation|tapeworm|roundworm|filariasis" --regex --shell Contact
```

`--in` controls **where** it looks. The default is `all`:

| `--in` | searches | notes |
|---|---|---|
| `all` *(default)* | filename, PresetName, opening note lines, **and all 71 MB of author prose** | column weights rank a name match above a prose match |
| `names` | filename and PresetName only | fastest, no prose |
| `notes` | prose only | rare; use when you specifically want the description |

**Do not use `--in names` as a default.** Measured: searching `enterobius` returns
**13** results with `names` and **53** with `all`. The 40 extra are exactly the
presets whose filename does *not* contain the term but whose author's prose does —
`Threadworms (C)` describes itself as *"pinworms (Enterobius vermicularis)"*, and
`Pinworm Infection (R)` is only reachable through prose. Authors routinely name the
exact organism **only in the description**, so a name-only search silently hides the
best-targeted presets in the corpus.

An earlier version of `--in notes` was implemented as a name filter ANDed with a
notes filter, which could only ever narrow the result set and never widen it — it
returned byte-identical output to the name-only search while appearing to work.
If a search mode returns suspiciously identical numbers to another mode, suspect
the filter, not the data.

---

## Rule 11 — verify before you recommend, it costs one query

A filename that does not exist cannot be recommended, and you can prove it in one
call. Real example: `Healing (L).txt` does **not** exist. The Healing shells in
this corpus are `Healing (C) - JW`, `Healing (R) - JW`, `Healing (R) - MM`,
`Healing (Dual) (R) - JW` and `Spooky Plasma Entrainment and Healing (P) - JW`.
There is no Laser Healing shell at all.

So before any filename goes into an answer:

```bash
python query.py find "<name fragment>" --regex --limit 5
```

Zero rows means the file is not there. Say so rather than offering it. Never
reproduce a filename that came from memory, from another AI's answer, or from
inference — **look it up**.

---

## Maintenance — rebuilding after a Spooky2 update

Spooky2 ships new preset material with releases. The JW Peptide collection landed
in 2026 and was entirely new, so assume the corpus changes without warning. When it
does:

```bash
cd <repo-root>/preset-db/tools
python rebuild.py            # detect corpus, build spooky-NEW.db, audit, print the diff
python rebuild.py --swap     # promote it, only after reading the diff
```

`rebuild.py` never overwrites the live database. It builds to `spooky-NEW.db`, runs
the full audit including the query-tool smoke test, and prints a content diff
against the current database: files added, **modified** (compared by content hash,
so an edited preset is caught, not just a new one) and removed, grouped by
collection, plus new or gone collections and authors.

`--swap` refuses to run if the audit fails, and keeps the previous database as a
dated `.bak`.

Details that matter:

- **The corpus path is discovered, never hardcoded.** Order: `--corpus`, then the
  `SPOOKY2_CORPUS` environment variable, then `S:\Spooky2\Preset Collections`, then
  Program Files, then a working copy next to the repo. It survives a Windows
  reinstall or a move to another drive.
- **`Preset Collections/User/` is skipped by default.** Those are the user's own
  presets, and folding them in makes "what does Spooky2 actually ship" unanswerable.
  Use `--include-user` to index them too.
- **The User's Guide is a separate problem.** If the guide is updated, re-render and
  re-read it rather than trusting this skill; the page citations below refer to the
  January 2025 edition.
- **Do not edit the corpus.** It is read-only input.

---

## Known gaps — do not paper over them

These are unresolved in the source material. State them rather than improvising:
`MW Emulate` vs `MW Remove` (undefined); **MOR — "Mortal Oscillatory Rate" is
never defined in 244 pages**; Reverse Lookup default tolerance has **three**
competing values (25 % p59, 0.0125 % p136, field shown as `.25` p120/p122); DNA
database size **151,857/43,058 in 2022 vs 79,527/29,051 in 2020**; the corpus
`Force_BP_to_Hz_Factor` of `4.35589935811E+17` matching **none** of the guide's
DNA/RNA/mRNA constants; Max HRV 30 vs 20; three sweep types vs two in the File
menu; water 6–8 vs 4–8 pints; the waveform count on p190 (9 vs 12); and whether
the Cancer / Morgellons & Lyme / full Detox protocols are in the User's Guide at
all (p5 lists separate Video, Simple, Technical and NanoGuides, so they probably
are not).

Already **resolved** and no longer gaps: `GX` = GeneratorX Pro offline storage;
`MN`/`BN` = waveform-graph port selectors, not mode tokens; `SS` and `FB` are
confirmed by Spooky2's own shipped shell filenames even though the guide never
mentions them; and `DH` (not `OH`) is confirmed by `DH_0001_01 GX Offline (R) - DH`
on p125.

The guide also never gives a worked DNA frequency, nor explains how a base-pair
count combines with the conversion factor — the largest remaining gap given that
22,985 of 48,463 presets are DNA programs. Full list with page numbers in
`docs/KNOWLEDGE.md` §12.
