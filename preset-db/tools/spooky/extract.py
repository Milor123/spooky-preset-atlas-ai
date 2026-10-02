"""Taxonomy derivation and rule-based metadata extraction.

Two principles:

* Determinism. Every tag, duration and warning is derived by an explicit rule over
  literal text, and every derived row keeps the snippet that produced it. Nothing
  is guessed from a model.
* No interpretation of proprietary notation. The letter codes inside frequency
  tokens are opaque program data and are never decoded here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

# Author codes observed in the corpus (filename suffix " - XX"). Only these are
# accepted, so a stem ending in an ordinary word cannot be misread as an author.
KNOWN_AUTHORS: dict[str, str | None] = {
    "JW": "John White",      # confirmed by JW_Peptides/JW Peptides - John White.pdf
    "EL": None,
    "DB": None,
    "BY": None,
    "JRG": None,
    "JD": None,
    "MM": None,
    "AR": None,
    "JK": None,
    "EV": None,
    "BR": None,
    "BEM": None,
    "WD": None,
    "DI": None,
    "JE": None,
    "AW": None,
    "KB": None,
    "SH": None,
    "RB": None,
    "DG": None,
    "JF": None,
    "LW": None,
    "DW": None,
    "CK": None,
    "NS": None,
    "BW": None,
    "PM": None,
    "DH": None,
    "MA": None,
}

SHELLS = {
    "Coil": "Coil / PEMF",
    "Contact": "Contact electrodes",
    "Plasma": "Plasma tube",
    "Remote": "Remote (Bioresonance)",
    "Scalar": "Scalar",
    "Laser": "Cold laser",
    "Footbath": "Footbath",
    "Audio": "Spooky Audio",
}

MODES = {
    "R": "Remote",
    "C": "Contact",
    "L": "Cold Laser",
    "SS": "Scalar",
    "P": "Plasma",
    "FB": "Footbath",
    "GX": "GX waveform",
    "XM": "XM waveform",
    "Dual": "Dual output",
    "Coil": "Coil",
    "Stun": "Stun",
    "EM": "Electro-Magnetic",
}

MODE_TOKEN_RE = re.compile(
    r"\((R|C|L|SS|P|FB|GX|XM|Dual|Coil|Stun|EM)\)", re.IGNORECASE
)
AUTHOR_SUFFIX_RE = re.compile(r"(?:^|[\s)\-])((?:[A-Z]{2,4}))\s*$")

# (slug, label, category, regex)
TAGGERS: list[tuple[str, str, str, re.Pattern[str]]] = [
    # --- organism ---------------------------------------------------------
    ("bacteria", "Bacteria", "organism", re.compile(r"\bbacteri|\bcolon(?:y|ies)\b", re.I)),
    ("virus", "Virus", "organism", re.compile(r"\bvirus(?:es)?\b|\bviral\b", re.I)),
    ("fungus", "Fungus", "organism", re.compile(r"\bfung(?:us|i|al)\b|\byeast\b|\bcandida|\bmold\b|\bmould\b", re.I)),
    ("parasite", "Parasite", "organism", re.compile(r"\bparasite|\btapeworm|\bpinworm|\bworm\b|\bprotozoa", re.I)),
    ("phage", "Phage", "organism", re.compile(r"\bphage", re.I)),
    ("biofilm", "Biofilm", "organism", re.compile(r"\bbiofilm", re.I)),
    ("mycotoxin", "Mycotoxin", "organism", re.compile(r"\bmycotoxin", re.I)),
    ("spirochete", "Spirochete", "organism", re.compile(r"\bspirochet|\blyme\b|\bborrelia", re.I)),
    ("amoeba", "Amoeba", "organism", re.compile(r"\bamoeba", re.I)),
    # --- condition --------------------------------------------------------
    ("cancer", "Cancer", "condition", re.compile(r"\bcancer|\bcarcinogen|\btumou?r\b|\boncolog", re.I)),
    ("covid", "COVID-19", "condition", re.compile(r"\bcovid|\bsars[- ]?cov", re.I)),
    ("detox", "Detox", "condition", re.compile(r"\bdetox|\bcleanse|\bpurge", re.I)),
    ("herx", "Herxheimer", "condition", re.compile(r"\bherx|\bjarisch", re.I)),
    ("morgellons", "Morgellons", "condition", re.compile(r"\bmorgellons", re.I)),
    ("lyme", "Lyme", "condition", re.compile(r"\blyme", re.I)),
    ("allergy", "Allergy", "condition", re.compile(r"\ballerg", re.I)),
    ("inflammation", "Inflammation", "condition", re.compile(r"\binflammat", re.I)),
    ("infection", "Infection", "condition", re.compile(r"\binfection", re.I)),
    ("pain", "Pain", "condition", re.compile(r"\bpain\b", re.I)),
    ("insomnia", "Insomnia", "condition", re.compile(r"\binsomnia|\bsleep\b", re.I)),
    ("stress", "Stress / Anxiety", "condition", re.compile(r"\bstress|\banxiet", re.I)),
    ("fatigue", "Fatigue", "condition", re.compile(r"\bfatigue|\bchronic fatigue|\bme/cfs", re.I)),
    ("metals", "Heavy Metals", "condition", re.compile(r"\bheavy metal|\bmetal(?:s)? detox|\bmercury", re.I)),
    # --- organ / system ---------------------------------------------------
    ("liver", "Liver", "organ", re.compile(r"\bliver|\bhepatic", re.I)),
    ("kidney", "Kidney", "organ", re.compile(r"\bkidney|\brenal", re.I)),
    ("lymph", "Lymphatic", "organ", re.compile(r"\blymph", re.I)),
    ("blood", "Blood", "organ", re.compile(r"\bblood\b", re.I)),
    ("brain", "Brain / CNS", "organ", re.compile(r"\bbrain|\bcns\b|\bneuro", re.I)),
    ("gut", "Gut", "organ", re.compile(r"\bgut\b|\bintestin|\bcolonic|\bgi tract", re.I)),
    ("lung", "Lung", "organ", re.compile(r"\blung|\bpulmonary|\brespirat", re.I)),
    ("heart", "Heart", "organ", re.compile(r"\bheart|\bcardiac", re.I)),
    ("thyroid", "Thyroid", "organ", re.compile(r"\bthyroid", re.I)),
    ("immune", "Immune system", "organ", re.compile(r"\bimmune", re.I)),
    ("skin", "Skin", "organ", re.compile(r"\bskin|\bdermat", re.I)),
    ("bone", "Bone", "organ", re.compile(r"\bbone|\bosteo", re.I)),
    ("prostate", "Prostate", "organ", re.compile(r"\bprostate", re.I)),
    ("eye", "Eye", "organ", re.compile(r"\beyes?\b|\bocular|\bretina", re.I)),
    ("joint", "Joints", "organ", re.compile(r"\bjoint|\barthritis", re.I)),
    ("nerve", "Nerves", "organ", re.compile(r"\bnerve|\bneuropath", re.I)),
    # --- protocol ---------------------------------------------------------
    ("biofeedback", "Biofeedback", "protocol", re.compile(r"\bbiofeedback|\bbioscan", re.I)),
    ("sweep", "Frequency sweep", "protocol", re.compile(r"\bsweep", re.I)),
    ("chain", "Preset chain", "protocol", re.compile(r"\bchain\b", re.I)),
    ("maintenance", "Maintenance", "protocol", re.compile(r"\bmaintenance|\bmaintain\b", re.I)),
    ("terrain", "Terrain protocol", "protocol", re.compile(r"\bterrain\b", re.I)),
    ("peptide", "Peptide", "protocol", re.compile(r"\bpeptide|\bproteody", re.I)),
    ("radionics", "Radionics", "protocol", re.compile(r"\bradionic|\bwilliam dowsing|\bdowsing", re.I)),
    ("dna", "DNA", "protocol", re.compile(r"\bdna\b|\bnucleo", re.I)),
    ("colour", "Colour / Chromotherapy", "protocol", re.compile(r"\bcolou?r\b|\bchromo", re.I)),
    ("essential-oil", "Essential oil", "protocol", re.compile(r"\bessential oil|\baromatherapy", re.I)),
    ("bach", "Bach flower", "protocol", re.compile(r"\bbach\b", re.I)),
    ("homeopathy", "Homeopathy", "protocol", re.compile(r"\bhomeopath|\bsuis\s+ke", re.I)),
    ("scalar", "Scalar", "protocol", re.compile(r"\bscalar\b", re.I)),
    ("plasma", "Plasma", "protocol", re.compile(r"\bplasma\b", re.I)),
    ("coil", "Coil / PEMF", "protocol", re.compile(r"\bcoil\b|\bpemf\b", re.I)),
    ("remote", "Remote", "protocol", re.compile(r"\bremote\b|\bbioresonance", re.I)),
]

DURATION_UNIT_MINUTES = {
    "second": 1 / 60,
    "minute": 1,
    "hour": 60,
    "day": 1440,
    "week": 10080,
    "month": 43200,
}

DURATION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "continuous",
        re.compile(
            r"as long as possible|as much as possible|continually|24\s*/\s*7|indefinitely|"
            r"until (?:you|it) (?:stop|recover)",
            re.I,
        ),
    ),
    ("as-needed", re.compile(r"\bas needed\b|\bwhenever needed\b|\bon demand\b", re.I)),
    (
        "window",
        re.compile(
            r"(\d{1,2}):(\d{2})\s*(am|pm)?\s*(?:-|–|to)\s*(\d{1,2}):(\d{2})\s*(am|pm)?",
            re.I,
        ),
    ),
    (
        "cadence",
        re.compile(r"\bevery\s+(\d+)\s+(second|minute|hour|day|week|month)s?\b", re.I),
    ),
    (
        "explicit",
        re.compile(
            r"\b(?:for|over|during|last(?:s|ing)?)\s+(\d+)\s*(second|minute|hour|day|week|month)s?\b",
            re.I,
        ),
    ),
    (
        "bare",
        re.compile(r"\b(\d+)\s*(second|minute|hour|day|week|month)s?\b", re.I),
    ),
]

WARNING_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("pregnancy", re.compile(r"\bpregnan|\bexpectant\b", re.I)),
    ("pacemaker", re.compile(r"\bpacemaker\b", re.I)),
    ("implant", re.compile(r"\bimplant|\bmetal in (?:the )?body\b", re.I)),
    ("blood-thinner", re.compile(r"\banticoagulant|\bblood thinner|\bwarfarin\b", re.I)),
    ("diabetes", re.compile(r"\bdiabet|\binsulin\b", re.I)),
    ("epilepsy", re.compile(r"\bepilep|\bseizure\b", re.I)),
    ("children", re.compile(r"\bchildren\b|\bchild\b|\binfants?\b|\btoddler", re.I)),
    ("pregnancy-suspected", re.compile(r"\bmiscarriage|\bfoetal?|\bfetus\b", re.I)),
    ("consult", re.compile(r"\bconsult (?:your|a|with)\b|\byour (?:doctor|physician)\b|\bmedical advice\b", re.I)),
    ("not-proven", re.compile(r"\bnot (?:a )?(?:proven|demonstrated|validated)\b|\bno evidence\b|\bnot a therapeutic\b", re.I)),
    ("do-not", re.compile(r"\bdo not (?:use|run)\b|\bdo not use\b", re.I)),
    ("avoid", re.compile(r"\bavoid\b", re.I)),
    ("caution", re.compile(r"\bcaution\b|\bwarning\b|\bbeware\b", re.I)),
]


@dataclass
class TagHit:
    slug: str
    label: str
    category: str
    source: str
    confidence: float
    evidence: str


@dataclass
class DurationHit:
    kind: str
    value_text: str
    minutes: int | None
    evidence: str


@dataclass
class WarningHit:
    kind: str
    evidence: str


# ---------------------------------------------------------------------------
# Taxonomy derivation
# ---------------------------------------------------------------------------

SHELL_ALIASES = {
    "remote": "Remote",
    "coil": "Coil",
    "contact": "Contact",
    "plasma": "Plasma",
    "scalar": "Scalar",
    "laser": "Laser",
    "shells": None,  # structural folder, not a shell name
}

MODE_TO_SHELL = {
    "R": "Remote",
    "C": "Contact",
    "L": "Laser",
    "SS": "Scalar",
    "P": "Plasma",
    "FB": "Footbath",
    "Coil": "Coil",
}


def derive_author(stem: str) -> str | None:
    """Accept only codes actually observed in the corpus."""
    stem = stem.strip()
    m = AUTHOR_SUFFIX_RE.search(stem)
    if not m:
        return None
    code = m.group(1).upper()
    if code in KNOWN_AUTHORS:
        return code
    # `... (C) EV` has no dash; retry after the last bracket.
    tail = re.split(r"[()]", stem)[-1].strip()
    token = tail.split()[-1].upper() if tail.split() else ""
    return token if token in KNOWN_AUTHORS else None


def derive_modes(stem: str) -> list[str]:
    seen: list[str] = []
    for m in MODE_TOKEN_RE.finditer(stem):
        raw = m.group(1)
        token = "Coil" if raw.lower() == "coil" else (
            "Dual" if raw.lower() == "dual" else raw.upper())
        if token not in seen:
            seen.append(token)
    if "Dual" not in seen and re.search(r"\bDual\b", stem):
        seen.append("Dual")
    return seen


def derive_shell(base_preset: str | None, path_segments: list[str], modes: list[str]) -> str | None:
    """Priority: Base_Preset (authoritative shell link) > folder > mode token."""
    if base_preset:
        for seg in re.split(r"[\\/]", base_preset):
            key = seg.strip().lower()
            if key in SHELL_ALIASES:
                shell = SHELL_ALIASES[key]
                if shell:
                    return shell
        for m in MODE_TOKEN_RE.finditer(base_preset):
            shell = MODE_TO_SHELL.get(m.group(1).upper())
            if shell:
                return shell

    for seg in path_segments:
        key = seg.strip().lower()
        if key in SHELL_ALIASES and SHELL_ALIASES[key]:
            return SHELL_ALIASES[key]

    for mode in modes:
        shell = MODE_TO_SHELL.get(mode)
        if shell:
            return shell
    return None


def notes_lead(notes: str, limit: int = 320, max_lines: int = 3) -> str:
    """First meaningful lines of the notes: a cheap, honest, non-invented summary."""
    if not notes:
        return ""
    kept: list[str] = []
    total = 0
    for raw in notes.splitlines():
        line = raw.strip()
        if not line:
            continue
        kept.append(line)
        total += len(line) + 1
        if len(kept) >= max_lines or total >= limit:
            break
    out = " ".join(kept)
    return out[:limit]


# ---------------------------------------------------------------------------
# Rule extraction
# ---------------------------------------------------------------------------


def extract_tags(
    free_text: str, path_segments: list[str], stem: str, preset_name: str
) -> list[TagHit]:
    hits: dict[tuple[str, str], TagHit] = {}

    # Folder and filename are literal author intent: confidence 1.0.
    for seg in path_segments:
        key = seg.lower()
        for slug, label, category, pat in TAGGERS:
            if pat.fullmatch(seg) or (len(seg) > 3 and pat.search(seg) and slug in slug):
                hits.setdefault(
                    (slug, "folder"),
                    TagHit(slug, label, category, "folder", 1.0, f"folder:{seg}"),
                )
        if key in {"dna", "cancers", "detox", "heal", "biofeedback"}:
            slug = key.rstrip("s")
            hits.setdefault(
                (slug, "folder"),
                TagHit(slug, slug.title(), "protocol", "folder", 1.0, f"folder:{seg}"),
            )

    for m in MODE_TOKEN_RE.finditer(stem):
        token = m.group(1).upper()
        if token in MODES:
            hits.setdefault(
                (f"mode-{token.lower()}", "filename"),
                TagHit(
                    f"mode-{token.lower()}", MODES[token], "delivery", "filename", 1.0,
                    f"filename token ({token})",
                ),
            )

    haystack = f"{preset_name}\n{stem}\n{free_text}"[:20000]
    for slug, label, category, pat in TAGGERS:
        if (slug, "folder") in hits:
            continue
        m = pat.search(haystack)
        if m:
            # Lower confidence than folder/filename: this is an inference from
            # prose, not an explicit statement of intent.
            hits.setdefault(
                (slug, "rule"),
                TagHit(slug, label, category, "rule", 0.45, m.group(0)[:160]),
            )
    return list(hits.values())


def extract_durations(notes: str) -> list[DurationHit]:
    hits: list[DurationHit] = []
    seen: set[tuple[str, str]] = set()
    for kind, pat in DURATION_PATTERNS:
        for m in pat.finditer(notes[:20000]):
            text = " ".join(m.group(0).split())
            minutes: int | None = None
            if kind in ("explicit", "bare", "cadence"):
                groups = m.groups()
                if len(groups) >= 2 and groups[0].isdigit():
                    minutes = int(round(int(groups[0]) * DURATION_UNIT_MINUTES[groups[1].lower()]))
            elif kind == "window":
                g = m.groups()
                try:
                    start = int(g[0]) * 60 + int(g[1])
                    end = int(g[3]) * 60 + int(g[4])
                    if g[2] and g[5]:
                        if g[2].lower() == "pm" and int(g[0]) < 12:
                            start += 720
                        if g[5].lower() == "pm" and int(g[3]) < 12:
                            end += 720
                    minutes = max(0, end - start)
                except (TypeError, ValueError):
                    minutes = None
            key = (kind, text.lower())
            if key in seen:
                continue
            seen.add(key)
            hits.append(DurationHit(kind, text[:160], minutes, text[:200]))
            if len(hits) >= 6:
                return hits
    return hits


def extract_warnings(notes: str, preset_name: str) -> list[WarningHit]:
    haystack = f"{preset_name}\n{notes}"[:20000]
    hits: list[WarningHit] = []
    for kind, pat in WARNING_PATTERNS:
        m = pat.search(haystack)
        if m:
            hits.append(WarningHit(kind, " ".join(m.group(0).split())[:200]))
    return hits