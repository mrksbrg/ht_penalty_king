"""Language packs for fem prickar.

Each language is a module exposing:
    NAME          -- human-readable language name
    SKILL_LEVELS  -- Hattrick skill denominations, index = level (0..20+)
    STRINGS       -- the full string table (see sv.py for the schema)

To add a language, copy sv.py to e.g. de.py, translate the values (keep the keys),
and run with  --lang de.  Strings are plain text so you can refine the wording
freely without touching code.
"""

AVAILABLE = ["sv", "en"]
