"""Derive a player's penalty 'profile' from their Hattrick attributes.

The guiding principle from the brief: attributes need not move the goal odds much,
but they should all be able to colour the *story*. So this module produces both a
set of numeric traits (0..1) used by the xG model and a list of Swedish report tags
used by the report engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .hrf_parser import Player

# Hattrick speciality code -> internal key
SPECIALTY = {1: "technical", 2: "quick", 3: "powerful", 5: "head", 4: "unpredictable"}


def _n(skill: int, top: int = 20) -> float:
    """Normalise a Hattrick skill (1..20+) to 0..1."""
    return max(0.0, min(1.0, skill / top))


def _nform(form: int) -> float:
    return max(0.0, min(1.0, form / 8.0))


@dataclass
class PenaltyProfile:
    player: Player
    # core competence
    general_class: float       # all-round footballing class (anti "usel överallt")
    penalty_technique: float   # how well they strike a penalty
    shot_power: float
    shot_placement: float
    composure: float           # nerve under the silly pressure
    chaos: float               # variance / unpredictability
    mind_game: float           # ability to get in heads
    # keeper side
    keeper_skill: float
    keeper_reading: float
    keeper_reach: float
    fatigue_resistance: float
    weak_foot_ability: float   # estimated competence on the weaker foot
    # life stage + flavour
    age_stage: str             # junior / prime / rutinerad / veteran / uråldrig
    specialty: str | None
    report_traits: list = field(default_factory=list)
    archetype: str | None = None   # combined-personality persona (see personality_archetype)


def _skills_norm(p: Player) -> list[float]:
    return [
        _n(p.keeper), _n(p.defending), _n(p.playmaking), _n(p.winger),
        _n(p.passing), _n(p.scoring), _n(p.set_pieces),
    ]


def _general_class(p: Player) -> float:
    s = sorted(_skills_norm(p), reverse=True)
    max_skill = s[0]
    top3 = sum(s[:3]) / 3.0
    return 0.6 * max_skill + 0.4 * top3


# Playable field positions, scored from skills. Order = GK → DEF → … → FWD.
POSITIONS = ["keeper", "defender", "wingback", "winger", "playmaker", "forward"]
# Full display/sort order, with the non-playing roles last.
POSITION_ORDER = POSITIONS + ["trainer", "former"]


def best_position(p: Player) -> str:
    """Approximate a player's best position from the seven skills (HO-style).

    Non-playing entries are caught first: a coach (TrainerType set in the HRF) is a
    'trainer', and an entry with no skills at all is a 'former' player — neither
    should be mistaken for a keeper just because every skill is zero.

    Otherwise: a weighted score per position over the raw skills, highest wins (ties
    resolve to the earlier, more defensive position). Returns a key from
    POSITION_ORDER."""
    if p.trainer:
        return "trainer"
    skills = (p.keeper, p.defending, p.playmaking, p.winger,
              p.passing, p.scoring, p.set_pieces)
    if max(skills) <= 0:
        return "former"
    scores = {
        "keeper": p.keeper,
        "defender": p.defending + 0.2 * p.set_pieces,
        "wingback": 0.7 * p.defending + 0.6 * p.winger,
        "winger": p.winger + 0.3 * p.passing + 0.2 * p.scoring,
        "playmaker": p.playmaking + 0.5 * p.passing,
        "forward": p.scoring + 0.3 * p.winger + 0.2 * p.playmaking,
    }
    return max(POSITIONS, key=lambda pos: scores[pos])


def personality_archetype(p: Player) -> str | None:
    """Combine the three personality axes into a single vivid persona, used to
    colour the big-moment commentary. Needs two strong axes to fire; returns the
    first matching archetype, else None for the unremarkable middle."""
    unpleasant, agreeable = p.agreeability <= 1, p.agreeability >= 4
    fiery, calm = p.aggressiveness >= 4, p.aggressiveness <= 1
    dishonest, honest = p.honesty <= 1, p.honesty >= 4

    if unpleasant and dishonest:
        return "villain"        # nasty and a cheat
    if fiery and dishonest:
        return "loose_cannon"   # explosive and sly
    if fiery and unpleasant:
        return "hothead"        # short fuse, no charm
    if agreeable and honest:
        return "gentleman"      # the nice, straight one
    if calm and (honest or agreeable):
        return "iceman"         # unflappable, principled
    if dishonest and calm:
        return "trickster"      # cold-blooded con artist
    return None


def _age_stage(years: int) -> str:
    if years <= 21:
        return "junior"
    if years <= 28:
        return "prime"
    if years <= 32:
        return "rutinerad"
    if years <= 36:
        return "veteran"
    return "uråldrig"


def _report_traits(p: Player, gc: float, specialty: str | None, stage: str) -> list[str]:
    t: list[str] = []
    # specialty
    if specialty:
        t.append("spec_" + specialty)
    # personality (use the HRF's own Swedish labels where telling)
    if p.agreeability <= 1:
        t.append("otrevlig")
    elif p.agreeability >= 4:
        t.append("sympatisk")
    if p.aggressiveness >= 4:
        t.append("temperamentsfull")
    elif p.aggressiveness <= 1:
        t.append("lugn")
    if p.honesty >= 4:
        t.append("arlig")
    elif p.honesty <= 1:
        t.append("ohederlig")
    # standing in the squad
    if p.homegrown or p.matches_team >= 150 or p.loyalty >= 18:
        t.append("trotjanare")
    if p.matches_team <= 25 and not p.homegrown:
        t.append("nyforvarv")
    if p.leadership >= 15:
        t.append("ledartyp")
    elif p.leadership <= 5:
        t.append("tystlaten")
    # status / money
    if p.salary >= 120_000 or p.market_value >= 25_000:
        t.append("dyrgrip")
    if gc <= 0.18:
        t.append("hopplos")        # genuinely useless all over
    elif _n(p.scoring) <= 0.15 and gc >= 0.5:
        t.append("klassspelare")   # great player, can't finish
    # life stage
    t.append("age_" + stage)
    # form extremes
    if p.form >= 7:
        t.append("hogform")
    elif p.form <= 3:
        t.append("lagform")
    return t


def derive_profile(p: Player) -> PenaltyProfile:
    gc = _general_class(p)
    sp_bonus = 0.15 if p.speciality == 3 else 0.0  # powerful
    specialty = SPECIALTY.get(p.speciality)
    stage = _age_stage(p.age_years)

    sp = _n(p.set_pieces)
    sc = _n(p.scoring)
    pa = _n(p.passing)
    pm = _n(p.playmaking)
    wg = _n(p.winger)
    kp = _n(p.keeper)
    df = _n(p.defending)
    ex = _n(p.experience)
    fm = _nform(p.form)

    penalty_technique = (
        0.40 * sp + 0.20 * sc + 0.12 * pa + 0.10 * pm + 0.08 * wg + 0.10 * gc
    )
    shot_power = 0.45 * sc + 0.25 * gc + 0.15 * fm + 0.15 * sp_bonus
    shot_placement = 0.45 * sp + 0.20 * pa + 0.15 * wg + 0.10 * pm + 0.10 * fm

    composure = (
        0.35 * ex + 0.20 * fm + 0.15 * _n(p.leadership)
        + 0.15 * _n(p.loyalty) + 0.15 * gc
    )
    # chaos: temperament, youth, unpredictability raise variance
    unpredictable = 1.0 if p.speciality == 4 else 0.0
    chaos = (
        0.35 * _n(p.aggressiveness, 5)
        + 0.25 * (1.0 - ex)
        + 0.20 * unpredictable
        + 0.20 * (1.0 - composure)
    )
    mind_game = (
        0.45 * (1.0 - _n(p.agreeability, 5))
        + 0.30 * _n(p.leadership)
        + 0.25 * (1.0 - _n(p.honesty, 5))
    )

    keeper_skill = (
        0.55 * kp + 0.12 * ex + 0.10 * df + 0.08 * pm + 0.08 * sp + 0.07 * gc
    )
    keeper_reading = 0.40 * ex + 0.30 * pm + 0.30 * kp
    keeper_reach = 0.60 * kp + 0.20 * gc + 0.20 * df
    fatigue_resistance = _n(p.stamina)

    # Hattrick has no footedness, so estimate weaker-foot competence.
    weak_foot_ability = (
        0.30 * pa + 0.20 * wg + 0.15 * pm + 0.15 * sp + 0.10 * sc + 0.10 * gc
    )

    traits = _report_traits(p, gc, specialty, stage)

    return PenaltyProfile(
        player=p,
        general_class=gc,
        penalty_technique=penalty_technique,
        shot_power=shot_power,
        shot_placement=shot_placement,
        composure=composure,
        chaos=min(1.0, chaos),
        mind_game=mind_game,
        keeper_skill=keeper_skill,
        keeper_reading=keeper_reading,
        keeper_reach=keeper_reach,
        fatigue_resistance=fatigue_resistance,
        weak_foot_ability=weak_foot_ability,
        age_stage=stage,
        specialty=specialty,
        report_traits=traits,
        archetype=personality_archetype(p),
    )


def profile_cache(players: list[Player]) -> dict:
    return {p.pid: derive_profile(p) for p in players}
