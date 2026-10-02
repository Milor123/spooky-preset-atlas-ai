-- Spooky2 preset database schema.
-- Lossless index over the READ-ONLY corpus at ../Preset Collections.
-- Rule: the database is a faithful index. It never invents, completes or
-- modifies a value. Every frequency row keeps raw_token verbatim.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
-- Taxonomy
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS collection (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    preset_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS author (
    id             INTEGER PRIMARY KEY,
    code           TEXT NOT NULL UNIQUE,
    confirmed_name TEXT,
    preset_count   INTEGER NOT NULL DEFAULT 0
);

-- Delivery shell. Derived from Base_Preset, then folder, then filename token.
CREATE TABLE IF NOT EXISTS shell (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Mode token found in parentheses in the filename: R, C, L, SS, P, Dual, FB, GX, XM.
CREATE TABLE IF NOT EXISTS mode (
    id       INTEGER PRIMARY KEY,
    token    TEXT NOT NULL UNIQUE,
    label    TEXT,
    note     TEXT
);

-- ---------------------------------------------------------------------------
-- Source file
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS source_file (
    id            INTEGER PRIMARY KEY,
    path          TEXT NOT NULL UNIQUE,   -- relative to corpus root, forward slashes
    filename      TEXT NOT NULL,
    stem          TEXT NOT NULL,          -- filename without .txt  (explicit requirement)
    dir_path      TEXT NOT NULL,
    byte_size     INTEGER NOT NULL,
    content_hash  TEXT NOT NULL,
    preset_count  INTEGER NOT NULL DEFAULT 0,
    section_count INTEGER NOT NULL DEFAULT 0
);

-- ---------------------------------------------------------------------------
-- Preset
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS preset (
    id             INTEGER PRIMARY KEY,
    source_file_id INTEGER NOT NULL REFERENCES source_file(id),
    ordinal        INTEGER NOT NULL,      -- position of this preset inside the file
    -- The full filename is authoritative and is NEVER truncated. "(R)" inside it
    -- means Remote, "(C)" Contact, "(Coil)" Coil, "(L)" Cold Laser, "(SS)" Scalar.
    -- The literal string is preserved as-is; shell/mode are ADDITIONAL columns, not
    -- a replacement for it.
    filename_full  TEXT NOT NULL,         -- e.g. "MX Ropeworm - JW.txt"
    filename_stem  TEXT NOT NULL,         -- e.g. "MX Ropeworm - JW"
    filename_slug  TEXT NOT NULL,         -- casefolded stem, for tolerant name search
    preset_name    TEXT,                  -- PresetName key; may differ from filename_stem
    base_preset    TEXT,
    author_id      INTEGER REFERENCES author(id),
    collection_id  INTEGER REFERENCES collection(id),
    shell_id       INTEGER REFERENCES shell(id),
    mode_id        INTEGER REFERENCES mode(id),
    l1 TEXT, l2 TEXT, l3 TEXT, l4 TEXT,   -- folder hierarchy below collection
    -- Author description. Preset_Notes when present; many presets have none, in
    -- which case it falls back to the filename stem so it is never empty when a
    -- meaningful name exists.
    description    TEXT,                  -- notes_lead, or filename_stem when there are no notes
    notes_full     TEXT,                  -- Preset_Notes verbatim, never summarised away
    notes_lead     TEXT,                  -- first meaningful lines of the notes, when present
    notes_len      INTEGER NOT NULL DEFAULT 0,
    has_description INTEGER NOT NULL DEFAULT 0,
    program_count  INTEGER NOT NULL DEFAULT 0,
    freq_count     INTEGER NOT NULL DEFAULT 0,
    -- Hot parameters promoted to real columns so they are indexable/filterable.
    schedule_run_for   TEXT,
    schedule_run_from  TEXT,
    schedule_run_to    TEXT,
    repeat_sequence    TEXT,
    repeat_chain       TEXT,
    dedupe_enabled     INTEGER,
    dedupe_tolerance   TEXT,
    -- Every remaining key, verbatim. Repeated keys become JSON arrays.
    params_json   TEXT NOT NULL DEFAULT '{}',
    -- Derived booleans: is_biofeedback, is_sweep, is_chain, is_dna, is_peptide, has_notes
    flags_json    TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_preset_file      ON preset(source_file_id);
CREATE INDEX IF NOT EXISTS ix_preset_author    ON preset(author_id);
CREATE INDEX IF NOT EXISTS ix_preset_collection ON preset(collection_id);
CREATE INDEX IF NOT EXISTS ix_preset_shell     ON preset(shell_id);
CREATE INDEX IF NOT EXISTS ix_preset_mode      ON preset(mode_id);
CREATE INDEX IF NOT EXISTS ix_preset_name      ON preset(preset_name);
CREATE INDEX IF NOT EXISTS ix_preset_slug      ON preset(filename_slug);
CREATE INDEX IF NOT EXISTS ix_preset_stem      ON preset(filename_stem);
-- Reverse index: every preset whose full filename contains a given literal token,
-- e.g. '(R)' or 'Dual'. Used when the query is phrased in terms of the filename.
CREATE INDEX IF NOT EXISTS ix_preset_stem_nocase ON preset(filename_stem COLLATE NOCASE);

-- ---------------------------------------------------------------------------
-- Program: one Loaded_Programs line, paired 1:1 with one Loaded_Frequencies line
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS program (
    id             INTEGER PRIMARY KEY,
    preset_id      INTEGER NOT NULL REFERENCES preset(id),
    ordinal        INTEGER NOT NULL,
    program_name   TEXT,
    -- The parenthesised suffix on a program name is its provenance: the Spooky2
    -- database it came from. XTRA, KHZ, CAFL, VEGA, RUSS, BIO, HC, MW, DNA,
    -- PROV, CUST, BFB, ALT, XTRA, SD. "Ropeworm (XTRA)" is an XTRA program; that
    -- is the same taxonomy as the 16 tickable databases in the guide (p64).
    database_tag   TEXT,
    freq_line_raw  TEXT                    -- the whole Loaded_Frequencies line, verbatim
);

CREATE INDEX IF NOT EXISTS ix_program_preset ON program(preset_id);
CREATE INDEX IF NOT EXISTS ix_program_tag    ON program(database_tag);
CREATE INDEX IF NOT EXISTS ix_program_name   ON program(program_name);

-- Spooky2's official glossary of the database abbreviations, with the number of
-- programs in this corpus that came from each.
CREATE TABLE IF NOT EXISTS database (
    code        TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    program_count INTEGER NOT NULL DEFAULT 0,
    preset_count  INTEGER NOT NULL DEFAULT 0,
    in_guide_16   INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_db_code ON database(code);

-- A preset's TITLE rarely names what it actually treats, but its program list
-- does. "Leaky Gut Healing Therapy (CL) - JD" sounds like a gut protocol until
-- you read that it loads "Ropeworm (XTRA)" and "Biofilms 01 (XTRA)". Without this
-- index a search for "ropeworm" cannot find that preset at all, because the word
-- appears in neither the filename nor the notes. rowid == program.id.
CREATE VIRTUAL TABLE IF NOT EXISTS programs_fts USING fts5(
    program_name,
    tokenize = "unicode61 remove_diacritics 2"
);

-- ---------------------------------------------------------------------------
-- Frequency: one comma-separated token
-- ---------------------------------------------------------------------------
-- notation      plain | tilde | backtick | unknown
-- hz_lo/hz_hi   populated ONLY for plain notation where the LHS is numeric.
--               NULL otherwise: the tilde and backtick letter codes are UNKNOWN
--               semantics and are deliberately not interpreted.
-- amplitude     populated only when the token carries an explicit =<number>.
-- codes         opaque letter codes (BC, BL, BLR, M, CM, W, F) as found.
-- nums_json     every numeric run in the token, order preserved, no claims.
-- parse_status  ok | partial | unparsed
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS frequency (
    id           INTEGER PRIMARY KEY,
    program_id   INTEGER NOT NULL REFERENCES program(id),
    ordinal      INTEGER NOT NULL,
    notation     TEXT NOT NULL,
    raw_token    TEXT NOT NULL,
    hz_lo        REAL,
    hz_hi        REAL,
    amplitude    REAL,
    modifiers    TEXT,
    codes        TEXT,
    nums_json    TEXT,
    parse_status TEXT NOT NULL DEFAULT 'ok'
);

CREATE INDEX IF NOT EXISTS ix_freq_program ON frequency(program_id);
CREATE INDEX IF NOT EXISTS ix_freq_notation ON frequency(notation);
CREATE INDEX IF NOT EXISTS ix_freq_hz       ON frequency(hz_lo);
CREATE INDEX IF NOT EXISTS ix_freq_status   ON frequency(parse_status);

-- ---------------------------------------------------------------------------
-- Guide documents (the 23 PDFs define the vocabulary)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS doc (
    id            INTEGER PRIMARY KEY,
    path          TEXT NOT NULL UNIQUE,
    filename      TEXT NOT NULL,
    collection_id INTEGER REFERENCES collection(id),
    byte_size     INTEGER,
    title         TEXT,
    summary       TEXT,
    is_authoritative INTEGER NOT NULL DEFAULT 0
);

-- ---------------------------------------------------------------------------
-- Tags (controlled vocabulary, rule-derived)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tag (
    id       INTEGER PRIMARY KEY,
    slug     TEXT NOT NULL UNIQUE,
    label    TEXT NOT NULL,
    category TEXT NOT NULL               -- organism | condition | organ | protocol | delivery | safety
);

CREATE TABLE IF NOT EXISTS preset_tag (
    preset_id  INTEGER NOT NULL REFERENCES preset(id),
    tag_id     INTEGER NOT NULL REFERENCES tag(id),
    source     TEXT NOT NULL,            -- folder | filename | rule
    confidence REAL NOT NULL DEFAULT 1.0,
    evidence   TEXT,
    PRIMARY KEY (preset_id, tag_id, source)
);

CREATE INDEX IF NOT EXISTS ix_preset_tag_tag ON preset_tag(tag_id);

-- ---------------------------------------------------------------------------
-- Duration / cadence and safety text, extracted by rule (never by LLM)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS preset_duration (
    id          INTEGER PRIMARY KEY,
    preset_id   INTEGER NOT NULL REFERENCES preset(id),
    kind        TEXT NOT NULL,           -- explicit | window | continuous | cadence
    value_text  TEXT NOT NULL,
    minutes     INTEGER,
    evidence    TEXT
);

CREATE INDEX IF NOT EXISTS ix_duration_preset ON preset_duration(preset_id);

CREATE TABLE IF NOT EXISTS preset_warning (
    id         INTEGER PRIMARY KEY,
    preset_id  INTEGER NOT NULL REFERENCES preset(id),
    kind       TEXT NOT NULL,
    evidence   TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_warning_preset ON preset_warning(preset_id);
CREATE INDEX IF NOT EXISTS ix_warning_kind   ON preset_warning(kind);

-- ---------------------------------------------------------------------------
-- Full-text search. Standalone (not external-content) so rebuilds are trivial.
-- ---------------------------------------------------------------------------

CREATE VIRTUAL TABLE IF NOT EXISTS preset_fts USING fts5(
    filename_stem,
    preset_name,
    notes_lead,
    notes_full,
    tokenize = "unicode61 remove_diacritics 2"
);

-- Separate index for the filename itself, so "search the name" never has to scan
-- the full-text index or pull the notes prose into the query.
CREATE VIRTUAL TABLE IF NOT EXISTS name_fts USING fts5(
    filename_stem,
    filename_slug,
    preset_name,
    tokenize = "unicode61 remove_diacritics 2"
);

-- ---------------------------------------------------------------------------
-- Build integrity report
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS build_stat (
    id    INTEGER PRIMARY KEY,
    label TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS parse_issue (
    id         INTEGER PRIMARY KEY,
    path       TEXT NOT NULL,
    line_no    INTEGER NOT NULL,
    kind       TEXT NOT NULL,
    detail     TEXT,
    excerpt    TEXT
);

CREATE INDEX IF NOT EXISTS ix_issue_kind ON parse_issue(kind);
CREATE INDEX IF NOT EXISTS ix_issue_path ON parse_issue(path);

-- Unrecognised frequency token shapes, so nothing is silently dropped.
CREATE TABLE IF NOT EXISTS unknown_shape (
    id        INTEGER PRIMARY KEY,
    notation  TEXT NOT NULL,
    shape     TEXT NOT NULL,
    hits      INTEGER NOT NULL,
    example   TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- Convenience views
-- ---------------------------------------------------------------------------

CREATE VIEW IF NOT EXISTS v_preset_catalog AS
SELECT
    p.id                AS preset_id,
    p.filename_full,
    p.filename_stem,
    p.preset_name,
    p.description,
    a.code              AS author,
    c.name              AS collection,
    s.name              AS shell,
    m.token             AS mode,
    p.l1, p.l2, p.l3,
    p.notes_lead,
    p.program_count,
    p.freq_count,
    p.notes_len,
    sf.path             AS source_path
FROM preset p
JOIN source_file sf ON sf.id = p.source_file_id
LEFT JOIN author a     ON a.id = p.author_id
LEFT JOIN collection c ON c.id = p.collection_id
LEFT JOIN shell s      ON s.id = p.shell_id
LEFT JOIN mode m       ON m.id = p.mode_id;

CREATE VIEW IF NOT EXISTS v_freq_lookup AS
SELECT
    p.id              AS preset_id,
    p.preset_name,
    p.filename_stem,
    pr.ordinal      AS program_ordinal,
    fr.ordinal      AS freq_ordinal,
    fr.notation,
    fr.hz_lo,
    fr.hz_hi,
    fr.amplitude,
    fr.modifiers,
    fr.codes,
    fr.raw_token,
    fr.parse_status
FROM preset p
JOIN program  pr ON pr.preset_id = p.id
JOIN frequency fr ON fr.program_id = pr.id;