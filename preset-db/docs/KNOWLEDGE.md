# Spooky2 Domain Reference

> Consolidated from a vision pass over all 244 pages of
> `Spooky2_Users_Guide_20250124.pdf` plus read-only analysis of the 43,397-file
> preset corpus. Every claim carries a page reference or is marked INFERENCE.
> This file is the resolved,
> contradiction-free version.
>
> **Two facts about this reference that matter:**
> 1. The guide is the *User's Guide* only. Per p5 it is one of several documents
>    (Video Guide, Simple Guide, Technical Guide, NanoGuides). **The Cancer,
>    Morgellons & Lyme and full Detox protocols are probably NOT in these 244
>    pages.** Terrain appears (p102) because it is described inside the chain
>    editor screenshot. Do not invent protocol content that is not cited here.
> 2. Where the guide and the corpus disagree, the guide wins on mechanism and the
>    corpus wins on naming. Several corpus tokens are undocumented by the
>    manufacturer; those are flagged as such throughout.

---

## 1. The two-axis problem

Spooky2's own framing (p5): *"kill pathogens **and** heal organs and systems."*
That single sentence is the axis every preset sits on, and it is not a label —
it is a mechanism (p107):

> *Frequency Multiplier* "transpose frequencies up so they're closer to a
> pathogen's fundamental Mortal Oscillatory Rate. Octaves or decades are best…
> **This is only for killing, not healing, which requires the unchanged
> frequency** since healing works by **entrainment** (for organs and systems) and
> the **'jackhammer effect'** for detox."

**Healing = entrainment toward a higher healthy frequency.** p35–36 gives the
worked example: 600 Hz healthy versus 598 Hz. Healing raises frequency toward
health; killing moves frequency to a pathogen's MOR; detox is a jackhammer.

Consequences the tool must honour:

- A preset containing `Frequency_Multiplier` is **never** a candidate for a
  healing objective. Killing is the only thing it is for.
- A sweep is **never** a healing instrument (p40): *"The Spectrum Sweeps are
  designed for killing. Most healing works through frequency entrainment, and
  sweeps don't work for this process."*
- "Detox" is a third thing, neither killing nor healing. Do not collapse it into
  either.

---

## 2. Delivery modes — the filename tokens

The corpus encodes the delivery device in the filename. The guide rarely defines
the tokens, so the authoritative source is **Spooky2's own shipped shell
presets** in `Shell (Empty) Presets/`, which name each one.

| Token | Shell | Device | Evidence |
|---|---|---|---|
| `(R)` | Remote | Spooky Remote pad via Boost `BN` socket | p20; `Shell (Empty) Presets/Remote/` |
| `(C)` | Contact | stainless cylinders / TENS pads via Boost High Power Contact, or Colloidal Silver port (weak) | p21 |
| `(P)` | Plasma | Spooky Central/Plasma, straight or Phanotron tube, rear HV sockets | p13, p24, p25 |
| `(Coil)` | Coil | PEMF puck, `BN` face to skin, runs direct off Out 1 | p22 |
| `(L)` | Laser | Cold Laser Wrist or Twin, off Out 1 | p23 |
| `(SS)` | Scalar | Scalar Transmitter (+ Receiver via `Ban-A`/`Ban-B`, or GX Pro G1+G2) | shell file `Scalar\Spooky Scalar General (SS) - JW.txt` |
| `(Dual)` | — | both outputs transmitting simultaneously; the word is never used in the guide, closest is `Out 2 = (Out 1)` | p208, p29 |
| `(FB)` | Footbath | **Not in the guide at all.** Confirmed only by the shell file `Footbath General (FB) - JW.txt` | shell file |
| `GX` | — | **Never defined by the guide.** Appears only as a `Load GX` button (p31) and `Turn GX displays OFF/ON` (p203). INFERENCE: GeneratorX Pro | p31, p203 |
| `XM` | — | the Spooky2-XM generator itself, 5 MHz | p11 |

### 2.1 Mode ranking, the guide's own words (p40)

> Plasma — *"quickest and most powerful"*
> Contact — *"next for speed and power"*, with a dynamic carrier
> Remote — *"has gained on contact mode… a winner"* on convenience
> Coil — relaxation, circulation, regeneration
> Scalar — *"powerful healing treatments"*, whole body
> Laser — superficial, blood perfusion

Canonical day (p40): *"one plasma or contact session daily, **then switch that
generator to Remote Mode**"* — the same idea as p13's *"run non-stop
detox/support Programs remotely during and after plasma sessions."*

**Spooky Boost (p12)** quadruples Contact power and doubles Remote power, and has
a dedicated colloidal-silver output. Ports: `OUT1, OUT2, PW_R, CONTACT 1,
CONTACT 2, SILVER, BN, MN`.

### 2.2 Mode substitution is never valid

The DH collection replicates **the same 412 programs across all six shells**
(Remote 412, Plasma 412, Laser 412, Contact 412, Coil 412, Scalar 411). So for
such a collection, "which preset" is nearly meaningless — the choice is *which
device you have*, not *which program*. Presenting six near-identical rows as
six options is noise. Same applies to `0062 Elim Spirochetes Candida,Yeast,
Parasites,Mold`, which exists as `(C)`, `(Coil)` and `(L)` with the same 199
frequencies.

---

## 3. Shell presets

> **A shell is an empty preset containing settings only, no programs** (p36,
> echoed p27). A shell is a *delivery recipe*, not a treatment. A factory preset
> = shell + pre-loaded programs. (p36 gloss "shell (empty preset)" — the corpus
> folder is named `Shell (Empty) Presets` because of this.)

The shells that matter, straight from the corpus and p98:

| Shell | Intent | Source |
|---|---|---|
| `Killing (R)` / `(C)` | "for killing pathogens" | p98 |
| `Healing (R)` / `(C)` | "healing and entrainment" | p98 |
| `Killing Low Freq` | killing, low band | shell file |
| `MW Emulate` / `MW Remove` | molecular-weight primitives — **semantics NOT defined by the guide** | see 3.1 |
| `DNA (R)` / `(C)` | DNA-addressed programs | shell file |
| `Angry DNA (P)` | plasma DNA variant | shell file |
| `GX Online or Offline` / `True Amplitude Modulation (GX)` | GeneratorX variants | shell file |
| `Contact Carrier Wave` | carrier-based contact | shell file |

Audio, Coil, Laser and Scalar have **no kill/heal split** (p98). Plasma splits
by **frequency band instead of by name**: Entrainment/Healing below 100 KHz,
Advanced above 100 KHz. Do not assume the name pattern generalises.

### 3.1 MW Emulate vs MW Remove — unresolved, do not invent

No page defines the difference. What *is* sourced:

- `MW` = Molecular Weight (p32)
- the only suppression primitive in the software is the checkbox
  `Apply Inhibit Factor to Harmful MW Substances` (p28)
- the two constants differ: **MW→Hz = 2.2523430883E+23** versus
  **MW Inhibit = √2 · 10^17** (these are the literal values in the corpus files,
  `Force_MW_to_Hz_Factor` / `Force_BP_to_Hz_Factor`)
- the only live `Remove …` shell observed anywhere is `1. Remove Metals` (p31)

INFERENCE (unconfirmed): *Remove* subtracts/inhibits an MW, *Emulate* synthesises
an MW signal. The tool must label this as unconfirmed.

### 3.2 Dose lives in the shell, not in the frequency list (p28, p37)

This is why two shells running identical programs behave differently. Four levers:

- `Dwell Multiplier` — scales per-frequency time (default dwell **180 s**)
- `Frequency Multiplier` — scales frequency, and is the **killing** primitive
- `Repeat Each Frequency / Program / Sequence / Chain`
- gating (4 Hz / 125 ms seen) and per-output octave-band clamping

All four are preserved in the corpus `params_json`, so this is directly queryable.

---

## 4. Waveforms → intent (p169–173, p190)

| Waveform | Guide's verdict |
|---|---|
| **Inverse Sawtooth** | **killing** — *"powerful killer"* |
| Sawtooth | healing, detox |
| Square / Square H-Bomb / Damped Square | killing, healing, detox (*Damped Square* is a "Spooky² exclusive") |
| Sine / Sine H-Bomb / Damped Sinusoidal | healing, detox, and killing at very high frequencies |
| Triangle | **mainly experimental** |

Other waveform facts:

- Sine is best at high frequencies (p197)
- Square H-Bomb may be *"too powerful for remote use"* (p197)
- Inverse wave "chainsaw" amplitude doubling: 10 V becomes 20 V **only** when
  `Out 2 = (Out 1 × 1) + 0` (p158, p159, p164)
- Spike injects one high-voltage spike at every positive and negative peak;
  mechanism stated as cell electroporation (p158)
- Waveform family gallery (p190–196): 9 base waveforms under F2=3×F1, plus
  **Holland 11th Harmonic** (F2=11×F1), DSB AM and SSB AM at 3× and 11×.
  p190 is internally inconsistent — "9 different waveforms" in the body versus
  "12 waveforms" in a callout box, and neither count includes Colloidal Silver,
  Square Harmonic or Lilly.
- **ILLEGIBLE, not guessed:** the row of unlabelled waveform thumbnails in the
  Settings waveform grid (p29, ~14 of them).
  → **SUPERSEDED: see §13.2.** The `Waveform Menus` dropdown at p113 lists them
  by name: `Colloidal_Silver`, `Alpha-Stim`, `Beamwave`, `DC`, `GoldDoublnSaw`,
  `GoldWave17-29`, `GoldWave17-29Tenth`, `H-Bomb_Sine`.

---

## 5. Program types

| Type | Behaviour |
|---|---|
| **Sweep** | killing instrument; Spectrum is the aggressive one. Types offered in the File menu: **Single (OUT1), Dual Converge, Dual Weighted** (p188). A "Linear Sweep" is *not* in the menu; the p9 feature list of Carrier/Spectrum/Linear is not fully reconciled — see §9 |
| **Wobble** | controlled frequency/amplitude variation. Defaults: amplitude wobble **10–15%**, frequency wobble **1%**, **16 steps** (p152). Trajectories: sawtooth / inverse sawtooth / triangle |
| **Feathering** | *random* wobble, as opposed to Wobble's *controlled*. `.02%` feathering described as *"Excellent for remote treatment"* (p152) |
| **Modulate** | frequency modulation. Carrier needs *"at least three minutes"* per frequency versus modulation's *"**eight seconds or less**… may explain why such sweeps have not produced 'spontaneous remissions'"* (p77) |
| **Pulse** | pulsed delivery; Spooky Pulse biofeedback limits **Min BPM 30, Max BPM 130, Max HRV 30** (p32) |
| **Harmonic / Holland** | F2 = 11 × F1 |

**Duty cycle (p177):** *"Duty Cycles of less than 50% are not really very useful"*;
preferred **over 50%**, with 67 / 72 / 81 / 93 % named as experienced-rifer
values. 0 % = no signal, 100 % = constant, "neither of which are useful in Rife
therapy."

> This is a **signal-design** rule and is deliberately kept separate from the
> **hardware** rule on p7 that caps Spooky Central/Plasma at 50 % duty, where
> exceeding it *damages the unit*. Do not conflate them.

**Guide declines to endorse two menu entries (p156):** Fibonacci and Natural Log
wobbles — *"One highly respected Rife developer recommends using it exclusively,
but **our tests do not lead us to concur**."* Useful for refusing to invent a
rationale for them.

---

## 6. Spectrum — the hard constraints

**Spectrum is a killer, not a healer (p184, verbatim):**

> "Its primary purpose is not to heal, not to support, not to detox. It's really
> meant to be an **executioner**… so whenever you use it, you should also run
> detox and support Programs."

**Amplitude dilution (p185):** generators max **20 V**. 1,024 simultaneous
frequencies ⇒ **0.01953125 V each**, explicitly *"no good in Contact Mode."*
Wide-spectrum programs belong on **Remote**, or via Spooky Central/Plasma.

**MOR tolerance = ±0.025 %** (Dr. Rife, p184). Worked examples: 150 Hz →
149.9625–150.0375; 1.5 MHz → 1,499,625–1,500,375, which *"will also kill
everything else whose MORs lie within that range."* Spooky2 can transmit up to
**25 million Hertz**; historical frequencies were built on machines capped at
10 kHz/100 kHz, so MHz MORs are sub-harmonics of them.

**Formulas (p186–187):**
```
FS          = Center × MOR tolerance
Spectrum %  = WCM × 100 × FS ÷ Center
WCM         = half the child count     (children go above AND below)
```
100 children ⇒ WCM 50. Worked: 1.5 MHz / ±0.025 % / 100 children ⇒ FS 375,
Spectrum 1.25 %. 500 Hz / ±0.025 % / 20 children ⇒ WCM 10, FS 0.125, Spectrum
0.25 %.

**The one fully documented sweep (p188–189) — Hulda Clark Dual Weight Sweep:**
76,000–880,000 Hz, tol .025 %, WCM 96, Spectrum 84.1 %, total duration
**00:55:34**, sweep speed 1.32778 Hz/s, sweep 475786.75→480213.25 Hz, FS 4187.5,
Spectrum amplitude **.208 V**, both amplitudes **20 V**, both outputs Sine,
`Out 2 = (Out1 × .25) + 358500 Hz`. **Requires a second Spooky Remote with DNA on
Out 2, or Spooky Boost.**

---

## 7. SAFETY — hard rules, all quotable

| # | Rule | Source |
|---|---|---|
| 1 | **Spectrum and overnight carrier sweeps are for use only in the absence of a reliable diagnosis.** Not a general panacea. They kill almost *all* bacteria — pathogenic **and** beneficial. Prolonged continuous use may damage the immune system unless supplemented with natural probiotics (fermented: sauerkraut, kefir dairy and/or water, kimchi, pickles). **No sweep continuously for more than one week**, except environmental use, and in no case other than an emergency | p7 |
| 2 | **Never use duty other than 50 % on Spooky Central/Plasma** — you damage the unit | p7 |
| 3 | **Do NOT uncoil the USB/BNC cables of Spooky Central/Plasma or remove the metal ring** — it shields from plasma-bulb interference | p7 |
| 4 | **Do NOT adjust the Spooky2-XM front panel** unless guided by tech support; it is designed to be fully software-controlled | p7 |
| 5 | **Zapping in Contact Mode: 7 minutes maximum, 21 minutes rest.** *"Zapping longer than 7 minutes in Contact Mode without the rest can result in burning yourself"* | p208 |
| 6 | An **unbalanced waveform** (nonzero offset, or Square duty ≠ 50 %) can burn in Contact Mode — *but see §9.3, this is not a mechanical block* | p208 |
| 7 | **NEVER use while pregnant** | p208 |
| 8 | **Pacemaker or heart problems ⇒ Remote Mode ONLY** | p208 |
| 9 | **NEVER place a TENS pad on neck or head** | p208 |
| 10 | **Do NOT tick `Remove Duplicate Frequencies` inside the Morgellons and Lyme Protocol** — the duplicates are deliberate | p107 |
| 11 | Choose *Do NOT sort frequencies* unless you are an experienced rifer — **frequency order within a program is meaningful** | p64, p107 |
| 12 | Loading or firing requires `Overwrite Generator`, the safety lock | p37, p30 |
| 13 | Never hand-edit Spooky Central/Plasma presets except `Schedule` and `Audio Options` | p29 |
| 14 | Old XM comm boards burn out if left off the power adapter | p238 |
| 15 | Drink pure water. **p7 says 6–8 pints/day, p240 says 4–8.** Conservative reading: use the higher figure. Reason given: flushes toxins and dead organisms, and improves electrical conductivity (which matters in Contact) | p7, p240 |
| 16 | **NEVER-TRANSMIT LIST (p140): "You should add the 1840 and 1910 — these are believed to cause malignancy growth."** The blacklist is global to all generators. **Verified present in the corpus: 1840 Hz occurs 83 times across 22 distinct presets. 1910 Hz does not occur at all (0 rows).** This is checkable against the database and must be checked before recommending anything | p140 |
| 17 | **In Contact Mode you must use a dynamic carrier** (square, worked Factor 512); not necessary in Remote | p149 |

---

## 8. Protocol ordering

**Golden Rule of Rifting (p222):** *"Work from smallest to largest"*, *"from the
inside to the outside, from the things contained to the container itself."*
Killing a large parasite first releases its own parasites into the bloodstream.
Sequence orderings should follow organism scale.

**Terrain chain, actual ChainEditor contents on `Terrain (R) - BY` (p102):**

```
 1, 2   Remove Metals                       (same program, twice)
 3      Remove Chemical Materials
 4, 5   Remove Systemic Toxins 1 / 2
 6.1+6.2 Remove Intestinal Toxins || Remove Systemic Toxins 3   (simultaneous)
 7      Parasites and Liver Function
 8      Kidney Function 1
 9.1+9.2 Kidney Function 2 || Cleanse Blood
10.1+10.2 Kidney and Liver Toxins || Intestinal Parasites
11.1/11.2 Lymphatic System
```
Order: **toxins → liver → kidney → blood → gut → lymph last.** Footer:
`Repeat Chain 0`, `Run For 24 hrs`, `Run From/To Midnight`,
**"Estimated time forever 11 days 00:00:00"**.

**Durations:**
- non-stop Remote treatment: *"keep your run time **as close to four hours as
  possible**"* (p106)
- Blood Purifier: **2 h/day for 21–30 days**, 27 V DC → 3.9 Hz biphasic AC (p108)
- **2–3 day trial per targeted program, then rotate** (p40) — a recommendation
  is a trial, not a regimen
- default dwell **180 s**

**Every kill needs a detox (p15)**: the named program is **`RX Herxheimer - DB`**,
triggered by a Herxheimer reaction, inside the Morgellons & Lyme Protocol. `RX `
is a filename prefix convention.

**Canonical remote premise (p39):** `(R)` presumes a DNA-bearing sample with a
**2–5 day** life. Nails are "forever". Hair carries only RNA and needs the root
bulb. Recommendation cadence must respect this.

---

## 9. How the software decides what to run

### 9.1 Reverse Lookup (p31, p37, p59, p60, p62, p120, p125, p135, p136)

It is a **frequency-set match against database entries**, not a name match. Its
own text: *"programs in the database that may match your found frequencies."*

- Controls: `Include Harmonics`, `Include Sub-Harmonics`, `Octave` dropdown,
  `% Tolerance`, `Include [n] Hz In Search`, `Go`.
  **CONFLICT: p59 reports the default tolerance as 25 %, p136 calls 0.0125 % the
  default. Do not assert one number. Note that 0.0125 % is half of the ±0.025 %
  MOR tolerance of §6, so these may be two different settings that the guide
  words confusingly.**
- Every hit is annotated with its octave: `Salmonella (Octave #3)`.
- Matches report a **tolerance band per hit**:
  `Matches found for 41,123 Hz: (41,117 Hz – 41,128 Hz)`.
- **`No matches found for X Hz` is a normal, expected outcome.**
- One hit can legitimately map to many unrelated programs — p62 shows
  Ulcerative Colitis, Stuttering, a parasite and Keratitis from a single
  frequency.
- Verbatim warning (p62): *"This is NOT a diagnostic tool… Reverse lookup does
  NOT mean you have these illnesses."*
- Timing is I/O-bound, not RAM-bound: 1:07–5:31 versus 38 s–3:33 for a plain
  load, scanning the single main database file `Frequencies.s2d` (p235, p243).

**Rule for the tool: never force a match. If the corpus has no preset for the
case, say so.**

### 9.2 Biofeedback loop (p59, p61, p62)

```
scan  →  Create Program window  →  BFB_Frequencies.csv
      →  program named "BFB [Log Name] Date Time"  →  findable by searching "BFB"
```

| Device | Reports | Range | Time | Setup |
|---|---|---|---|---|
| **GeneratorX Pro** | `Value is Current - RA (%)` | 41 kHz – 1.8 MHz | ~29 min | TENS pads to Out 1. **Spooky Boost must NOT be used — it interferes** |
| **Spooky Pulse** | `Value is BPM - RA (%)` | 76 – 152 kHz (XM only) | ~47 min | sensor on **earlobe or finger**; pads as far apart as possible |
| Sample Digitizer | biofeedback on **fluid samples** (mucus, blood, urine); can treat the sample remotely if it contains viable DNA | | | p11 |
| Scalar Digitizer | see guide | | | p9 |

**"Mortal Oscillatory Rate" is never defined anywhere in the 244 pages.** The
GUI reports an `RA (%)` reading only. Treat MOR as the guide's *term* for a
pathogen's fundamental frequency without a supplied definition — do not invent
one.

### 9.3 Two traps to avoid

- **The offset/amplitude trap.** p175: XM spans −10 V to +10 V = **20 Vpp**. At
  amplitude setting 20 with 100 % offset the output is **10 Vpp, not 20**. Any
  "20 V" claim about an offset preset is wrong. The corpus stores `Out1_Offset`
  and `Out1_Amplitude`, so the real Vpp is computable.
  **Do not mechanically block Contact presets on nonzero offset** — the guide's
  own Clark Zapper uses 100 % positive offset in Contact. Duration (rule 5) is
  the real lever.
- **The sorting trap.** Frequency order inside a program is meaningful and
  Spooky2 will reorder frequencies unless told not to. Never sort a program's
  frequencies in the database or in any output.

---

## 9b. Waveform index → database keys (p136)

The guide numbers the waveforms 1–11 in program text, and the corpus stores
waveform selection as `Out1_*` / `Out2_*` parameters. The mapping is exact:

| Index | Guide name | Corpus key |
|---|---|---|
| 1 | Sine | `Out1_Sine` |
| 4 | Inverted Sawtooth | `Out1_Inverted_Sawtooth` |
| 5 | Triangle | `Out1_Triangle` |
| 6 | Damped Sinusoidal | `Out1_Sine_Damped` |
| 7 | Damped Square | `Out1_Square_Damped` |
| 8 | H-Bomb Sinusoidal | `Out1_Sine_Hbomb` |
| 9 | H-Bomb Square | `Out1_Square_Hbomb` |
| 10, 11 | User Defined 1, 2 | `Out1_User_Defined_1`, `Out1_User_Defined_2` |

`Cx = 1` means turn gating on.

**Limitation, and it is large:** these keys appear in only a small minority of
presets (`Out1_Offset` in 1,338, `Out1_Square` in 456 of 48,463). Most presets
inherit their waveform from `Base_Preset`. So the waveform→intent verdict in §4
can only be applied when the key is explicitly present; otherwise follow the
`Base_Preset` chain to the shell, and if that chain is unresolved, say so
instead of assuming.

## 9c. The five conversion factors (p138, p142)

| Factor | Guide value | In the corpus |
|---|---|---|
| DNA | 3.06735269246603E+17 | not stored under this name |
| RNA / mRNA | 3.74222102678858E+17 | not stored under this name |
| **MW → Hz** | 2.2523430883E+23 | `Force_MW_to_Hz_Factor` = `2.2523430883E+23` ✔ exact match |
| **MW Inhibit** | √2 · 10^17 | `Force_BP_to_Hz_Factor` = `4.35589935811E+17` — **does not match any guide constant** |
| DNA → Hz | — | `Force_BP_to_Hz_Factor` = `4.35589935811E+17` |

Each is "the calculated result when the number of base pairs is 1". These affect
**MW and DNA programs only, never Main**.

**CONFLICT:** the corpus ships one BP factor, `4.35589935811E+17`, which matches
none of the three DNA/RNA/mRNA constants in the guide. Either the software
changed after the guide was written, or the factor is applied differently. Do
not assert that corpus DNA programs use the guide's DNA constant.

`MW Inhibit` is described as a first-class operation (p142): *"apply this factor
to MW frequencies to inhibit the harmful effects of the molecule."* This is the
best available candidate for what `MW Remove` shells do — still INFERENCE.

## 9d. Frequency ceilings and named effects

- **XM hard limit: 5 MHz.** Up to **25 MHz** via Wave Cycle Multiplication
  (WCM = number of sub-waves per cycle, worked value 5). Above 25 MHz power
  attenuates and waveforms deform (p148, p149).
- **Transposition is killing-only, stated twice (p107, p149).** `Frequency
  Multiplier` defaults to 1, worked value 1024; the goal is to lift the
  program's *lowest* frequency into MHz.
- **Scoon Effect (p147):** 1 Hz offset between two outputs, Factor 1. The guide
  itself says the story is *"possibly apocryphal"* but that *"some highly
  experienced researchers swear by it."* Shell presets live in `Miscellaneous`.
  Same recipe as two-subject Contact (p150); only the 1 Hz differs.
- **Holland 11th Harmonic (p146):** two mechanisms — `Add F1 to F2` (additive) or
  `Modulate F2 Using F1 (AM DSB)` (variable carrier, *"a world-first"*). Shells
  in `Miscellaneous`.
- **Biofeedback (p131):** `Max Hits to Find` × **3 minutes** each; `Decimal
  Places` 5 below 600 Hz and 2 above; `Run Cycles 0` = repeat until stopped;
  `Start Delay` measured in heartbeats (20 assisted, 200 alone).
- **Generator states (p137):** 7,200 s (2 h) start delay; `VG` = Virtual
  Generator / Generator Shadowing; `Hold` is distinct from `Pause`.

## 13. Settings, waveform menus, amplitude bands, frequency limits (p109–p118)

### 13.1 The nine built-in waveforms and their default WCM (p113)

Sine · Square · Sawtooth · **Inverted Sawtooth** · Triangle · Sine Damped ·
Square Damped · Sine H-Bomb · Square H-Bomb

| Waveform | default WCM |
|---|---|
| Sine, Square, Sawtooth, Inverted Sawtooth, Triangle | **1** |
| Sine Damped, Square Damped | **8** |
| Sine H-Bomb, Square H-Bomb | **16** |

**Verified against the corpus:** `Sine_WCM` / `Square_WCM` / `Triangle_WCM` are
mostly `1`, but authors deliberately deviate — `Square_WCM=13` in 39 presets and
`Triangle_WCM=7` in 39 presets. Those are the *"integers like 3, 7, 11"* the
guide recommends for F2 Control (§13.5). The defaults are defaults, not rules.

**`Spectrum %` hard-requires `WCM > 1`** (p115): *"A value higher than 1 for WCM
must be used."* Corpus-checkable.

### 13.2 The `Waveform Menus` dropdown (p113) — this closes an earlier gap

`Colloidal_Silver` · `Alpha-Stim` · `Beamwave` · `DC` · `GoldDoublnSaw` ·
`GoldWave17-29` · `GoldWave17-29Tenth` · `H-Bomb_Sine`

**Six of these eight are defined nowhere else in the guide.** Only `Alpha-Stim`
and `H-Bomb_Sine` map to anything named elsewhere. This replaces the earlier
"waveform grid thumbnails illegible" gap from p29.

### 13.3 `Harmonic Menus` (Frequency Limits), 8 entries (p117)

`8x` · `Octave` · `Decade` · `Fibonacci` · `Golden Ratio` · `Odd` ·
`Natural Log*` · `Scalar*`

**Only Natural Log and Scalar carry the asterisk** — *"neither of these were
proven to our satisfaction."* `Golden Ratio` and `Odd` are **endorsed,
unstarred**.

**Verified against the corpus:** `Out1_Frequency_Limit_Harmonic_Type` stores
exactly these strings — `Octave` (215 presets), `Odd` (81), `Scalar*` (8),
`Fibonacci` (2), `Decade` (2) — **including the asterisk**. Strong confirmation
that the guide documents this dropdown accurately.

### 13.4 Amplitude bands and the required delivery parameters (p110)

| Mode | Amplitude |
|---|---|
| Contact | **14–20 V** |
| Remote | *"most people use 4-10"* |
| Plasma / Scalar | **require** one of: 5 V @ 100 % offset · 10 V positive-offset-only custom · 20 V negative-offset-only |
| Cold Laser | −100 % offset |
| Clark programs | 100 % / −100 % offset |

**The `Padlock` (p110)** *"prevents Amplitude, Offset, and Waveform from being
changed by the program."* This is the mechanism by which a shell pins its
delivery parameters — the software-level explanation of §3.2. It may not be
stored under an obvious corpus key; unverified.

**Polarity is encoded two ways (p114):** `+`/`−` polarity radio buttons *"can be
used in lieu of a 100% offset waveform."* Any validator checking the amplitude
table above must accept **both** encodings or it will produce false negatives.

### 13.5 `F2 Control` — the Contact dynamic-carrier mechanism (p118)

`F2 Control` *"automatically adds a high frequency dynamic carrier to each
frequency in your program."* This is how the p149 rule *"In Contact Mode, you
must use a dynamic carrier"* is actually implemented. Recommended multipliers:
octave, decade, and *"integers like 3, 7, 11"* — **11 is the Holland 11th
Harmonic**.

### 13.6 Frequency limits emit frequencies that are NOT in the program (p118)

This is the single most consequential operational fact in this section, and it
was derived by bunny from a worked example and then **verified arithmetically**.

Worked case, `Botulinum VEGA`, 518 Hz with band 76,000–880,000:

| System | Result |
|---|---|
| 8x | 265,216 |
| Octave | 132,608 |
| Decade | 518,000 |
| Fibonacci | 120,694 |

**The rule:** multiply by the lowest member of the chosen system that lands inside
the band; transmit the original on one Out and the product on the other.

> **Corollary: a preset with non-zero frequency limits emits frequencies that do
> not appear anywhere in its program list.** 61 presets in this corpus have
> `Out1_Min_Freq > 0`. For those, listing the program's frequencies is **not** the
> full picture of what is transmitted, and the tool must say so rather than imply
> the program list is complete.

**The mortal bandwidth (p117):** *"Dr. Rife and Dr. Clark found that frequencies
that killed pathogens lay between **76,000 Hz and 880,000 Hz**… their mortal
bandwidth."* Historical cap stated as 100 kHz. (This is the same 76,000–880,000
band as the Hulda Clark Dual Weight Sweep of p188.)

### 13.7 More delivery safety

| Rule | Source |
|---|---|
| `Swap Waveform Every` — *"used for Contact Mode to prevent **acid burns** on sensitive skin… **60 seconds for contact treatment, and 300 seconds for silver**"* | p111 |
| `Reduce Amplitude <` — *"because low frequencies can sting and tingle uncomfortably… **10 KHz is the default**… lowering the value about 1 kHz at a time"* | p117 |
| `Spike Length` — *"Higher values may be useful in Remote Mode, but could be **tingly in Contact Mode**"*; p162 adds that a value of 24 *"would be a good value to [avoid]… likely to be painful for contact mode"* | p114, p162 |
| **Spike Ratio changes real Vpp:** spike V = Amplitude, remainder = Amplitude ÷ Ratio. At Ratio 2 / amplitude 20 the span is **30, not 20** — extends the offset trap of §9.3 | p114 |

### 13.8 Scheduling precedence (p116)

`Run For [x] Hours` *"will override any Repeat Sequence settings already
entered."* `Stop When Complete` lets the current program finish. `Start In`
countdown requires ticking `Overwrite Generator` then `Start`.

`Restore Defaults` resets the whole Settings tab (p112). `Wobble` menu is exactly
`Disabled / Sawtooth / Inverted Sawtooth / Triangle`.

## 15. Reverse Lookup semantics, and the biofeedback protocol (p119–p129)

### 15.1 `Harmonic Type` is `Decade` as well as `Octave` (p125)

The dropdown is captioned `Octave` but includes **`Decade`**. Match-set cardinality
is a function of this choice — `Octave` roughly doubles, `Decade` roughly
multiplies by ten. **Record the setting with every result**, otherwise the
result count is meaningless.

`Include Harmonics` / `Include Sub-Harmonics` expand the **database** frequencies,
not the query. That is the mechanical cause of the p62 behaviour where one
frequency yields Ulcerative Colitis, Stuttering, a parasite and Keratitis.

**Reverse Lookup needs no scan and no running generator** (p125): it works *"even
if the Generator Pane is currently empty."* That is the legitimate,
non-diagnostic way to use it.

### 15.2 What a "hit" is (p127)

**Defined:** a hit is among the **N strongest matches (10 or 20), ranked by
response magnitude — not by severity.** A first scan is explicitly incomplete:
*"clear the stage … like peeling an onion, layer by layer."*

So one scan is not an answer, and response magnitude is not a measure of how sick
anyone is.

### 15.3 The scan cadence protocol (p127, verbatim)

| Mode | Cadence |
|---|---|
| **Plasma** | **1×/day for 4 days** |
| **Contact** | **1×/day for 7 days** |
| **Remote** | **non-stop for 1 week** |

The resulting program goes in **"a killing preset"** — **it is not a sweep.** A
biofeedback result is a targeted program, not a broad kill.

### 15.4 `GX` is DEFINED (p125) — closes a long-open gap

`GX` = **GeneratorX Pro offline program storage**. Two spellings: `GX Offline`
and `GenX Offline`.

**Hard allow-list (p126):** GX stores **Frequency, Waveform, Amplitude, Offset,
Duty Cycle, Gate and Dwell only.** **Sweeps, chains and repeat settings cannot be
loaded into it.** So a corpus preset carrying `GX`/`XM` in its name is limited to
a single program with no chaining.

### 15.5 `MN` / `BN` resolved (p119) — not mode tokens

They are **waveform-graph port selectors**, unrelated to the delivery-mode
filename tokens. This retires the question.

`DH` confirmed independently: p125 shows a program named
`DH_0001_01 GX Offline (R) - DH`, settling `OH` vs `DH` in favour of **DH**.

### 15.6 Cardiac safety controls (p128, p129)

- **`Double HRV Tolerance`** is a **cardiac safety gate**, not a scan parameter.
- A maximum **`BPM`** setting exists.
- **A negative `BPM` or `HRV` reading is a sensor error, not a reading** (p129).
  Machine-checkable: never treat a negative as data.
- TENS pad placement: right hand / left ankle (p129), pairing with the
  never-on-neck-or-head rule (p208).

### 15.7 Two traps in reading the interface

- **`Age Factor` is a TEST SPEED MULTIPLIER, not the patient's age** (p124).
- **Object hierarchy is Chain → Preset → Program → Frequency** (p124), and
  **`Preset = 1` is the "not in a chain" sentinel** — a software-internal
  convention unrelated to this database's `preset.ordinal`.

### 15.8 The 4-hour session is arithmetic (p125)

`Frequency Count 80 × Dwell 180 s = 4 h exactly` in the guide's own screenshot.
The canonical *"as close to four hours as possible"* Remote session is therefore
usually a **product of two settings**. Multiply it out; do not trust a "4 hour"
label.

## 16. Databases

The `Database` pane has **16 tickable** entries (p64):
`ALT, BFB, BIO, CAFL, CUST, DNA, ETDFL, HC, KHZ, MW, PROV, RIFE, RUSS, SD, VEGA,
XTRA`. Reverse Lookup runs over 12 and **excludes DNA, MW and BP**.

Meanings (p105):
`ALT` Ayurvedic/solfeggio · `CAFL` · `DNA` ~108,000 frequencies ·
`MW` ~17,000 drug/supplement/molecule frequencies · `PROV` · `RIFE` · `RUSS` ·
`VEGA` · `ETDFL` · `KHZ`/`HC` Hulda Clark · `BFB`/`SD` biofeedback ·
`CUST` team and personal · `BIO` · `XTRA`

Active store counts seen live (p27): `DNA 151,857` · `Non-Human DNA 43,058` ·
`MW 13,913` · `Main 10,097` · `Encyclopedia 9,169`, Programs tab 59,800.
`DNA + MW + Main + Encyclopedia = 185,036`, which almost certainly reconciles
the *"more than 185,000 entries in five databases"* of p9 — so the 16 tickable
entries are content tags/filters, not the five main stores. This reconciliation
is an INFERENCE from arithmetic, not a stated fact.

**Custom databases (p81–p85):** four custom DBs; #2–#4 *selectable*, #1–#4
*editable*. Column schema: **Col 1 = program name, Col 4 = notes, Col 5 =
frequency list, Col 8 = default dwell.** `Write Database Text` exports name +
duration + description. `Extract Preset Frequencies` → `PresetPrograms.csv`.
Spectrum-sweep dialogs state *"The program will be saved in the Custom
database"* (p78).

Files: main DB `Frequencies.s2d` (p235); three shipped custom CSVs —
`Lyme Research Custom.csv`, `Misc Custom.csv`, `Morgellons Research.csv` in
`Documents > Custom Databases` (p236). MW/DNA frequencies are deliberately
hidden in the Programs pane and encrypted on the Generator Control Panel (p108).

> These are the **software's** databases. They are a different thing from the
> 43,397 preset files in the corpus. Never conflate them.

---

## 10b. Program names, database provenance, chains (measured)

**Program names are a semantic index the title understates.** Verified case:
`Miscellaneous/Johannes_D/Cold Laser/Leaky Gut Healing  Therapy (CL) - JD.txt`
loads `ATP Generate (XTRA)`, `Leaky Gut Sweep (XTRA)`, **`Ropeworm (XTRA)`**,
`Biofilms 01 (XTRA)`, `Intestinal Inflammation (VEGA)`, `Colitis - Inflammation
(RUSS)`, `Inflammatory Bowel Diseases (KHZ)`, `Harmony (XTRA)`, `Schumann's
resonance (BIO)`. The word "ropeworm" appears in neither the filename nor the
notes, so a name or prose search cannot reach it.

All 174,623 program names are now indexed (`programs_fts`, rowid = `program.id`),
reachable with `query.py find "<term>" --in programs`. It is **opt-in, not the
default**, and it always prints which program matched — a hit without evidence is
noise; a hit with evidence is the strongest signal available, because the title
understates and the program list does not.

**Measured reach:** for `ropeworm OR biofilm OR parasite OR worm`, 1,565 presets are
reachable in total and only **3** are reachable *solely* by subprogram. So the deep
search barely widens results. Its value is precision, not recall: it finds the
occasional preset whose title understates its contents.

**Database provenance.** The parenthesised suffix on a program name is the
Spooky2 sub-database it came from. Spooky2's own glossary has **17** codes; the
p64 pane lists **16** and omits `RRM`. Observed in this corpus:

| code | programs | presets using it |
|---|---|---|
| CUST | 24,760 | 23,992 |
| XTRA | 3,838 | 707 |
| CAFL | 829 | 412 |
| MW | 785 | 86 |
| HC | 373 | 202 |
| KHZ | 284 | 183 |
| PROV | 197 | 110 |
| BIO | 124 | 91 |
| VEGA | 35 | 30 |
| DNA | 31 | 8 |
| ALT | 18 | 18 |
| RUSS | 17 | 10 |
| BFB | 3 | 3 |
| RIFE | 1 | 1 |
| ETDFL, RRM, SD | 0 | absent from this corpus |

31,295 of 174,624 programs carry a tag; the rest are untagged custom programs.
`CUST` includes the user's own personal database. Spooky2 describes `BIO` and
`VEGA` in near-identical words; that duplication is in their published text and is
left as published. `MW` is given as ~8,000 programs here, ~9,000 on p138 and ~17,000
on the website — record all three, assert none.

**Chains are an attribute, not a search dimension.** A chain is a numbered protocol
run in order (`1. R05 Immunomodulators`, `2. R05…`, `3. R05…`, `4. R06 Viruses A`…),
not a program that references others. `Contact Plus Support Gen1 (R) - BY.txt` holds
222 such presets. Search it and you get the same file 222 times. The database
already models it correctly: 48,463 rows, one per preset, `is_chain` as a flag.

## 11. The authority tiers (tool-side, not from the guide)

The guide documents Spooky2's own mechanism. The corpus contains author-made
presets that carry **no manufacturer endorsement at all**. A recommendation must
say which tier it came from.

| Tier | What it is | How to present |
|---|---|---|
| **1** | Spooky2's own documented mechanism and built-in databases | As software behaviour, with a page |
| **2** | Author collection with its own PDF, named in the guide — e.g. **DH-0001…DH-0006**, which p101 calls *"most popular presets to chain"* | Attribute to the author; guide-blessed |
| **3** | Experimental / undocumented author work — DH-0007 onward, `FB`, `GX` | **Label experimental, not manufacturer-validated** |
| **4** | Non-medical: aura, chakras, meridians, energies | **Label as author energy-work claim, never as treatment** |

`DH Experimental Frequencies` = **David Halliday** (p100 lists
`Experimental Frequencies - David Halliday.pdf`; p101 praises DH-0001→DH-0006).
The folder is 2,472 presets / 2,466 programs / 53,706 frequencies, and its first
programs are `0001 Spiritual Wellbeing`, `0002 Combined 7 Chakras + Meridians`,
`0003 Remove Negative Energies`, `0004 Aura Clear Energetic Body`, `0005 Higher
Chakras Universal Divinity Connection`, `0006 Protection of Aura & Light Body` —
**Tier 4**, despite being the ones the guide names. From 0007 it becomes
conventional (`Alkalize`, `Oxygenize`, `Breathing`, `Headaches & Migraine`).

---

## 12. Known contradictions and gaps — do not paper over these

1. **Three sweep types vs two.** p9 lists **Carrier, Spectrum and Linear**. The
   File menu (p69) offers only `Create Carrier Sweep` and `Create Spectrum
   Sweep`. `Linear` appears only as the `xxx-yyy` syntax in the Create Program
   legend. The p188–189 sweep dialogs offer Single / Dual Converge / Dual
   Weighted. Unreconciled — state all readings with their page.
2. **Reverse Lookup default tolerance: THREE candidate values, none confirmed.**
   p59 reports **25 %**, p136 calls **0.0125 %** the default, and p120/p122
   screenshots show the field literally as `.25`. Note `.025 %` also appears on
   p120 in the scan pane, and 0.0125 % is half the ±0.025 % MOR tolerance (§6).
   These may be different settings worded confusingly. **Assert no number.**
3. **DNA database size: 151,857 / 43,058 dated 20220209 (p138) vs 79,527 / 29,051
   dated 20200501 (p141).** Never assert one number.
4. **Corpus `Force_BP_to_Hz_Factor` = 4.35589935811E+17 matches none of the
   guide's DNA/RNA/mRNA constants** (§9c).
5. **Max HRV: 30 (p138) vs 20 (p140 screenshot).**
6. **Water intake**: 6–8 pints (p7) vs 4–8 (p240).
7. **`OH` vs `DH Experimental Frequencies`: RESOLVED in favour of DH.** p125
   shows a program named `DH_0001_01 GX Offline (R) - DH`, independently of the
   p100/p101 references to David Halliday. The earlier "OH" was a misread.
8. **`MW Emulate` vs `MW Remove`**: undefined. §3.1.
9. **`GX`: RESOLVED, see §15.4** — GeneratorX Pro offline program storage, with
   a hard allow-list that excludes sweeps, chains and repeat settings.
10. **Waveform count**: 9 vs 12 on p190. §4.
11. **Mortal Oscillatory Rate**: never defined. §9.2.
12. **The guide never gives a worked DNA frequency**, nor explains how a base-pair
    count combines with the conversion factor. Biggest remaining gap given that
    22,985 of the 48,463 presets are DNA programs.
13. **Protocol collections** (Cancer, Morgellons & Lyme, full Detox) are probably
    in the *other* guides described on p5, not in these 244 pages.
14. **`CAFL`, `WCM`** — acronyms never expanded. `WCM` is functionally
    established (§13.1: Wave Cycle Multiplication, the sub-wave count).
    **`MN`/`BN` are RESOLVED — see §15.5**: waveform-graph port selectors, not
    mode tokens. `VI Angle` remains undefined; `Alpha-Stim` is at least a real,
    selectable waveform per §13.2. The `3,100,000` value in the `Out 1 fixed at`
    field (p146, p147, p150) is never explained in prose.
15. **Settings waveform grid thumbnails (p29, ~14)** — named in §13.2 via the
    p113 dropdown.
16. **p12/p13 Spooky Central front-panel silkscreen and the rear yellow
    warning-triangle text are illegible.**
17. **`Generator Shadowing` contradiction:** p111 calls it *"planned for a later
    edition"*, while p137 treats `VG` as "Virtual Generator / Generator
    Shadowing". Unreconciled.
18. **`Padlock`** (p110) — no confirmed corpus key yet; unverified.
19. **`BLx`, `BCx`, `Lx`, `Mx`** frequency-definition symbols (p111) — the page
    they hyperlink to lies outside the range read.
20. **p127 layout garbled in places:** the GeneratorX Pro scan time and the
    Central/Plasma sentence are not legible because words are split across line
    breaks. Three device photos on p125 have illegible branding.
21. **One guide-internal error, flagged not resolved:** p125 item 36 says
    `Decrease GX Calibration` *"increases"*, which is self-contradictory.
