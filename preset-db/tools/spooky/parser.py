"""Deterministic reader for Spooky2 preset .txt files.

The format is a quoted VB6-style INI dialect:

    "[Preset]"
    "Key=Value"
    "Multiline_Key=first line
    ...more lines...
    "
    "[/Preset]"

Two quirks drive this parser:

1. Section markers are QUOTED. A bare `[Preset]` on its own line does not open a
   section. Some older files also carry unquoted `[GEN1]`-style markers, so both
   spellings are accepted but only `[Preset]` opens a preset.
2. A value whose opening line does not end in a closing quote continues over
   several lines and is terminated by the first line that ends with a closing
   quote. The corpus uses two spellings of that: a bare `'"'` line (JW_Peptides)
   or a final prose line that simply ends in `'"'` (Biofeedback). As a safety net
   a line that starts a new key also closes the pending value. Preset_Notes uses
   this for the long prose blobs; an unterminated value is reported, never
   silently swallowed.

3. Key names may contain `%`, e.g. `BFB_Initial_Step_Size_%`.

Nothing here interprets frequency semantics. Tokens are classified by their
leading character and every numeric run is preserved verbatim.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from typing import Iterator

# Keys that legitimately repeat many times inside one preset.
MULTIVALUED_KEYS = frozenset(
    {
        "Loaded_Programs",
        "Loaded_Frequencies",
        "Preset_Notes",
        "Program_Description",
    }
)

# A program name ends in the Spooky2 database it came from: "Ropeworm (XTRA)".
# That suffix is provenance, and it is also the same taxonomy the guide calls the
# 16 tickable databases (p64): ALT, BFB, BIO, CAFL, CUST, DNA, ETDFL, HC, KHZ,
# MW, PROV, RIFE, RUSS, SD, VEGA, XTRA.
_DB_TAG_RE = re.compile(
    r"\((ALT|BFB|BIO|CAFL|CUST|DNA|ETDFL|HC|KHZ|MW|PROV|RIFE|RRM|RUSS|SD|VEGA|XTRA)\)\s*$")

# Spooky2's own glossary of the abbreviated database names, quoted verbatim. A
# program name carries its origin in a parenthesised suffix, so "Ropeworm (XTRA)"
# tells you it came from the XTRA sub-database. This is Spooky2's text, not ours.
#
# Two notes recorded rather than corrected:
#   * Spooky2 describes BIO and VEGA with near-identical wording ("frequencies
#     based on excellent Russian frequency research"). That duplication is in their
#     text and is left as published.
#   * RRM appears here but NOT in the guide's list of 16 tickable databases (p64).
#     The official glossary has 17. Trust the glossary.
#   * MW is given as "about 8,000 programs" here, as ~9,000 on p138 and ~17,000 on
#     the website. Record all three; assert none.
DB_GLOSSARY: dict[str, str] = {
    "ALT":   "programs based on Ayurvedic knowledge and practice, solfeggios, and "
             "planetary frequencies",
    "BFB":   "a collection of biofeedback scan results",
    "BIO":   "a collection of frequencies based on excellent Russian frequency research",
    "CAFL":  "the Consolidated Annotated Frequency List, amassed over years from the "
             "experience of Rife experimenters",
    "CUST":  "programs added by Spooky team members, plus those in your own personal "
             "database",
    "DNA":   "a massive collection of programs for human, animal, and plant pathogens "
             "based on DNA dimensions",
    "ETDFL": "a collection of programs researched in bio resonance clinics in Germany",
    "HC":    "the Dr. Hulda Clark database. Use with HC or KHZ (R) - JK preset",
    "KHZ":   "a collection of higher frequencies from Dr. Hulda Clark",
    "MW":    "a collection of about 8,000 programs for drugs, supplements, and "
             "molecules important to health",
    "PROV":  "has produced consistent results in virtually all subjects it was used with",
    "RIFE":  "a collection of original frequencies from Dr. Royal Raymond Rife",
    "RRM":   "comprehensive pathogen-disabling frequencies derived using proprietary "
             "JW_RRM methods",
    "RUSS":  "programs were extracted from various Russian databases",
    "SD":    "programs derived from biofeedback scans using Spooky Digitizer",
    "VEGA":  "a collection of frequencies based on excellent Russian frequency research",
    "XTRA":  "a collection of programs from various sources, all chosen for their "
             "reputation for effectiveness",
}


def database_tag(program_name: str | None) -> str | None:
    """Return the Spooky2 database a program name says it came from."""
    if not program_name:
        return None
    m = _DB_TAG_RE.search(program_name.strip())
    return m.group(1) if m else None

_SECTION_RE = re.compile(
    r'^\ufeff?"\[([^\]]+)\]"\s*$|^\ufeff?\[([^\]]+)\]\s*$'
)
_KEY_RE = re.compile(r'^"([A-Za-z_0-9%]+)=(.*)$')
_BARE_KEY_RE = re.compile(r'^([A-Za-z_0-9%]+)=(.*)$')

PRESET_SECTION = "Preset"


@dataclass
class Issue:
    path: str
    line_no: int
    kind: str
    detail: str = ""
    excerpt: str = ""


@dataclass
class ParsedPreset:
    ordinal: int
    keys: dict[str, list[str]] = field(default_factory=dict)
    issues: list[Issue] = field(default_factory=list)

    def first(self, key: str, default: str | None = None) -> str | None:
        vals = self.keys.get(key)
        return vals[0] if vals else default

    def all(self, key: str) -> list[str]:
        return self.keys.get(key, [])


@dataclass
class ParsedFile:
    path: str          # relative to corpus root, forward slashes
    content_hash: str
    byte_size: int
    presets: list[ParsedPreset]
    other_sections: list[str]
    issues: list[Issue]


def _strip_trailing_quote(value: str) -> str:
    return value[:-1] if value.endswith('"') else value


def parse_text(text: str, path: str, content_hash: str, byte_size: int) -> ParsedFile:
    """Parse one preset file into its preset blocks."""
    issues: list[Issue] = []
    presets: list[ParsedPreset] = []
    other_sections: list[str] = []

    current: ParsedPreset | None = None
    pending_key: str | None = None
    pending_parts: list[str] = []
    pending_line = 0

    for line_no, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()

        # ---- value accumulation ------------------------------------------------
        if pending_key is not None:
            # Safety net: a new key closes the pending value and is then handled
            # as a key in this same iteration.
            if _KEY_RE.match(raw) or _BARE_KEY_RE.match(raw):
                current.keys.setdefault(pending_key, []).append(
                    "\n".join(pending_parts)
                )
                pending_key, pending_parts = None, []
            elif stripped.endswith('"'):
                pending_parts.append(_strip_trailing_quote(raw))
                current.keys.setdefault(pending_key, []).append(
                    "\n".join(pending_parts)
                )
                pending_key, pending_parts = None, []
                continue
            else:
                pending_parts.append(raw)
                continue

        # ---- section markers ---------------------------------------------------
        m = _SECTION_RE.match(stripped)
        if m:
            name = m.group(1) or m.group(2)
            if name == PRESET_SECTION:
                current = ParsedPreset(ordinal=len(presets))
                presets.append(current)
            elif name.startswith("/"):
                current = None
            else:
                other_sections.append(name)
                current = None
            continue

        if not stripped:
            continue

        if current is None:
            # Content outside any preset block. Only flag it if it looks like a
            # key/value pair, which means we lost track of the section structure.
            km = _BARE_KEY_RE.match(stripped)
            if km:
                issues.append(
                    Issue(path, line_no, "key_outside_preset", km.group(1), stripped[:120])
                )
            continue

        # ---- key line ----------------------------------------------------------
        km = _KEY_RE.match(raw) or _BARE_KEY_RE.match(raw)
        if not km:
            issues.append(Issue(path, line_no, "unrecognised_line", "", stripped[:120]))
            continue

        key, value = km.group(1), km.group(2)
        if value.endswith('"'):
            current.keys.setdefault(key, []).append(_strip_trailing_quote(value))
            continue

        # Value continues on the following lines.
        pending_key, pending_parts, pending_line = key, [value], line_no

    if pending_key is not None:
        current.keys.setdefault(pending_key, []).append("\n".join(pending_parts))
        issues.append(
            Issue(
                path,
                pending_line,
                "unterminated_value",
                pending_key,
                pending_parts[0][:120] if pending_parts else "",
            )
        )

    for p in presets:
        p.issues = issues
    return ParsedFile(
        path=path,
        content_hash=content_hash,
        byte_size=byte_size,
        presets=presets,
        other_sections=other_sections,
        issues=issues,
    )


UTF8_BOM = b"\xef\xbb\xbf"


def decode_corpus_bytes(data: bytes) -> str:
    """Decode a corpus file without corrupting it.

    A number of files start with a UTF-8 BOM. Decoded as latin-1 the BOM becomes
    three visible characters in front of the first ``"[Preset]"`` marker, which
    stops the section detector and silently empties the whole preset. Detect the
    BOM and decode as UTF-8 in that case; everything else is treated as latin-1
    so no byte is ever lost.
    """
    if data.startswith(UTF8_BOM):
        try:
            return data[len(UTF8_BOM):].decode("utf-8")
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1")


def read_and_parse(abs_path: str, rel_path: str) -> ParsedFile:
    with open(abs_path, "rb") as fh:
        data = fh.read()
    content_hash = hashlib.sha256(data).hexdigest()
    text = decode_corpus_bytes(data)
    # Defensive: strip a BOM that survived a mis-decode on the very first line.
    if text.startswith("\ufeff"):
        text = text[1:]
    elif text.startswith("\ufffd"):
        text = text[1:]
    pf = parse_text(text, rel_path, content_hash, len(data))
    pf.byte_size = len(data)
    return pf


# ---------------------------------------------------------------------------
# Frequency tokens
# ---------------------------------------------------------------------------

_NUM_RE = re.compile(r"\d+(?:\.\d+)?")
_LETTER_RE = re.compile(r"[A-Za-z]+")
_RANGE_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$")
_PLAIN_NUM_RE = re.compile(r"^(\d+(?:\.\d+)?)$")


@dataclass
class FreqToken:
    ordinal: int
    raw: str
    notation: str
    hz_lo: float | None = None
    hz_hi: float | None = None
    amplitude: float | None = None
    modifiers: str | None = None
    codes: str | None = None
    nums: list[str] = field(default_factory=list)
    parse_status: str = "ok"


def classify_notation(raw: str) -> str:
    if raw.startswith("`"):
        return "backtick"
    if raw.startswith("~"):
        return "tilde"
    return "plain"


def tokenize_frequencies(line: str) -> list[FreqToken]:
    """Split one Loaded_Frequencies value into tokens.

    A nested backtick may appear inside a token (`` `...BC`m ``), so the split is
    on commas only; the token keeps its backticks verbatim in raw.
    """
    tokens: list[FreqToken] = []
    for ordinal, piece in enumerate(line.split(",")):
        raw = piece.strip().rstrip('"').strip()
        if not raw:
            continue
        tokens.append(_parse_token(raw, ordinal))
    return tokens


def _parse_token(raw: str, ordinal: int) -> FreqToken:
    notation = classify_notation(raw)
    nums = _NUM_RE.findall(raw)
    codes = "".join(_LETTER_RE.findall(raw))

    tok = FreqToken(
        ordinal=ordinal,
        raw=raw,
        notation=notation,
        codes=codes or None,
        nums=nums,
    )

    # The tilde and backtick notations carry letter codes whose meaning is not
    # documented in the corpus. They are recorded, never interpreted.
    if notation in ("tilde", "backtick"):
        tok.parse_status = "partial"
        return tok

    lhs, _, rhs = raw.partition("=")
    lhs = lhs.strip()
    rhs = rhs.strip()

    if rhs:
        parts = rhs.split()
        head = parts[0]
        if _PLAIN_NUM_RE.match(head):
            tok.amplitude = float(head)
            tok.modifiers = " ".join(parts[1:]) or None
        else:
            tok.modifiers = " ".join(parts)
            tok.parse_status = "partial"
    else:
        tok.parse_status = "partial"

    rng = _RANGE_RE.match(lhs)
    if rng:
        tok.hz_lo, tok.hz_hi = float(rng.group(1)), float(rng.group(2))
    elif _PLAIN_NUM_RE.match(lhs):
        tok.hz_lo = tok.hz_hi = float(lhs)
    else:
        tok.parse_status = "partial"

    if not nums:
        tok.parse_status = "unparsed"
    return tok


def token_shape(raw: str) -> str:
    """Collapse a token to its digit-agnostic shape, for the unknowns report."""
    return _NUM_RE.sub("#", raw)


# ---------------------------------------------------------------------------
# Corpus walking
# ---------------------------------------------------------------------------


def iter_corpus_files(root: str, extensions: tuple[str, ...] = (".txt",)):
    """Yield (abs_path, rel_path) for every corpus file, deterministically ordered."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.lower().endswith(extensions):
                continue
            abs_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(abs_path, root).replace(os.sep, "/")
            yield abs_path, rel_path