"""Hattrick CountryID -> (English name, ISO-3166 alpha-2) and a flag emoji.

Hattrick assigns each nation a sequential id (Sweden was first, id 1). The HRF only
stores the numeric CountryID, so we resolve a display name + flag from this table.

The table is intentionally easy to extend: add `id: ("Name", "ISO2")` rows. Unknown
ids degrade gracefully to a neutral flag and a dash, so an incomplete table never
breaks the UI. The authoritative full list is Hattrick's CHPP `worlddetails.asp`
(field LeagueID/CountryID + EnglishName); paste more rows in as needed.
"""

from __future__ import annotations

# CountryID -> (English name, ISO 3166-1 alpha-2 code)
# Seeded with Sweden (confirmed id 1, the founding league). Extend freely.
COUNTRIES: dict[int, tuple[str, str]] = {
    1: ("Sweden", "SE"),
}


def _flag(iso2: str) -> str:
    """Turn an ISO-3166 alpha-2 code into a flag emoji (regional indicators)."""
    iso2 = iso2.strip().upper()
    if len(iso2) != 2 or not iso2.isalpha():
        return "🏳️"
    return "".join(chr(0x1F1E6 + (ord(c) - ord("A"))) for c in iso2)


def nationality(country_id: int) -> dict:
    """Resolve a Hattrick CountryID to {id, name, flag} for display.

    Unknown ids fall back to a neutral flag and a dash so the UI stays clean."""
    name, iso2 = COUNTRIES.get(country_id, ("—", ""))
    return {"id": country_id, "name": name, "flag": _flag(iso2) if iso2 else "🏳️"}
