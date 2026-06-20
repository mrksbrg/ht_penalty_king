"""Read a Hattrick HRF export and turn its [player*] sections into Player objects.

Skill-key mapping (verified against Hattrick Organizer source HRFStringBuilder.java /
Player.java):

    mlv -> KeeperSkill        bac -> DefenderSkill
    mal -> ScorerSkill        spe -> PlaymakerSkill
    fas -> SetPiecesSkill      fra -> PassingSkill
    ytt -> WingerSkill         uth -> StaminaSkill
    for -> Form                rut -> Experience
    led -> Leadership          loy -> Loyalty
    sal -> Salary              mkt -> MarketValue
    ska -> InjuryLevel (-1 = fit)

Personality (numeric code + Swedish label straight from the HRF):
    gentleness/gentlenessLabel        -> agreeability   (otrevlig .. sympatisk)
    Aggressiveness/AggressivenessLabel-> aggressiveness (lugn .. temperamentsfull)
    honesty/honestyLabel              -> honesty        (ohederlig .. ärlig)
    speciality/specialityLabel        -> specialty
"""

from __future__ import annotations

import configparser
import glob
import os
import re
from dataclasses import dataclass


@dataclass
class Player:
    pid: int
    name: str
    age_years: int
    age_days: int
    # the seven skills
    keeper: int        # mlv
    defending: int     # bac
    playmaking: int    # spe
    winger: int        # ytt
    passing: int       # fra
    scoring: int       # mal
    set_pieces: int    # fas
    # condition / character
    stamina: int       # uth
    form: int          # for
    experience: int    # rut
    leadership: int    # led
    loyalty: int       # loy
    # status
    salary: int        # sal
    market_value: int  # mkt
    # personality (code + Swedish label)
    speciality: int
    speciality_label: str
    agreeability: int
    agreeability_label: str
    aggressiveness: int
    aggressiveness_label: str
    honesty: int
    honesty_label: str
    # misc
    warnings: int
    homegrown: bool
    matches_team: int
    injury: int        # ska (-1 = fit)

    @property
    def fit(self) -> bool:
        return self.injury < 0


def find_latest_hrf(directory: str, team_id: str | None = None) -> str:
    """Return the newest HRF in *directory*, chosen by the date in the filename."""
    pattern = os.path.join(directory, f"{team_id or '*'}-*.hrf")
    files = glob.glob(pattern)
    if not files:
        files = glob.glob(os.path.join(directory, "*.hrf"))
    if not files:
        raise FileNotFoundError(f"No .hrf files found in {directory!r}")

    date_re = re.compile(r"(\d{4}-\d{2}-\d{2})")

    def sort_key(path: str):
        m = date_re.search(os.path.basename(path))
        return (m.group(1) if m else "", os.path.getmtime(path))

    return max(files, key=sort_key)


def _read_config(path: str) -> configparser.RawConfigParser:
    """RawConfigParser avoids '%' interpolation; try utf-8 then latin-1."""
    for encoding in ("utf-8", "latin-1"):
        cp = configparser.RawConfigParser()
        cp.optionxform = str
        try:
            with open(path, "r", encoding=encoding) as fh:
                cp.read_file(fh)
            return cp
        except (UnicodeDecodeError, configparser.Error):
            continue
    cp = configparser.RawConfigParser()
    cp.optionxform = str
    with open(path, "r", encoding="latin-1", errors="replace") as fh:
        cp.read_file(fh)
    return cp


def _as_int(value: str | None, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def parse_players(path: str) -> list[Player]:
    """Parse every [player<id>] section in the HRF into a Player."""
    cp = _read_config(path)
    players: list[Player] = []
    for section in cp.sections():
        if not section.lower().startswith("player"):
            continue
        try:
            pid = int(re.sub(r"\D", "", section))
        except ValueError:
            continue

        def gi(k, d=0):
            return _as_int(cp.get(section, k, fallback=str(d)), d)

        def gs(k, d=""):
            return cp.get(section, k, fallback=d).strip()

        name = gs("name")
        if name.lower().startswith("null "):
            name = name[5:].strip()
        if not name or name.lower() == "null":
            name = gs("lastname") or f"#{pid}"

        players.append(
            Player(
                pid=pid,
                name=name,
                age_years=gi("ald"),
                age_days=gi("agedays"),
                keeper=gi("mlv"),
                defending=gi("bac"),
                playmaking=gi("spe"),
                winger=gi("ytt"),
                passing=gi("fra"),
                scoring=gi("mal"),
                set_pieces=gi("fas"),
                stamina=gi("uth"),
                form=gi("for"),
                experience=gi("rut"),
                leadership=gi("led"),
                loyalty=gi("loy"),
                salary=gi("sal"),
                market_value=gi("mkt"),
                speciality=gi("speciality"),
                speciality_label=gs("specialityLabel"),
                agreeability=gi("gentleness"),
                agreeability_label=gs("gentlenessLabel"),
                aggressiveness=gi("Aggressiveness"),
                aggressiveness_label=gs("AggressivenessLabel"),
                honesty=gi("honesty"),
                honesty_label=gs("honestyLabel"),
                warnings=gi("warnings"),
                homegrown=gs("homegr").lower() == "true",
                matches_team=gi("MatchesCurrentTeam"),
                injury=gi("ska", -1),
            )
        )
    if not players:
        raise ValueError(f"No [player*] sections found in {path!r}")
    return players


def team_name(path: str) -> str:
    cp = _read_config(path)
    return cp.get("basics", "teamName", fallback="Your team").strip()
