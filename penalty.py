"""Penalty Engine v2 — a sequence of football decisions instead of a flat
shooter-minus-keeper probability.

    select_shot_type()      what the shooter tries
    select_keeper_response() how the keeper guesses (reads body language, not the future)
    generate_shot_quality()  how well it is executed
    resolve()                outcome from (placement vs keeper) x quality

A side-foot can be a legendary placement or an air-shot; the keeper can guess
right and still be beaten by a perfect strike. That separation is what makes the
commentary varied.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from .config import Config
from .profiles import PenaltyProfile

SHOT_TYPES = [
    "instep_drive", "sidefoot", "curl", "panenka", "wait_out_keeper",
    "toe_poke", "chip", "center_blast", "center_placement",
]
QUALITIES = ["catastrophic", "poor", "average", "good", "excellent", "legendary"]

# central vs side shot tendencies (used to work out keeper "match")
_CENTER_SHOTS = {"panenka", "chip", "center_blast", "center_placement"}
_SIDE_SHOTS = {"instep_drive", "sidefoot", "curl"}
# shots beaten by a patient / central keeper rather than a side dive
_ADAPTIVE_SHOTS = {"wait_out_keeper"}

KEEPER_RESPONSES = [
    "stay_central", "dive_left", "dive_right", "delay_then_dive",
    "read_shooter", "gamble",
]

# outcome resolution tables, indexed by quality 0..5 (tune later; shape matters)
_P_MISS = [0.55, 0.25, 0.08, 0.03, 0.01, 0.00]
_P_GOAL_MATCHED = [0.05, 0.15, 0.30, 0.50, 0.75, 0.95]
_P_GOAL_UNMATCHED = [0.20, 0.55, 0.82, 0.92, 0.97, 0.995]

# execution quality shape (probabilities for catastrophic..legendary)
_DIST_STRONG = [0.02, 0.08, 0.20, 0.35, 0.25, 0.10]
_DIST_WEAK = [0.08, 0.20, 0.35, 0.25, 0.10, 0.02]


@dataclass
class DuelContext:
    attempt_number: int
    keeper_prickar: int
    weaker_foot: bool
    alive: int


@dataclass
class PenaltyResult:
    shot_type: str
    keeper_response: str
    quality: str            # one of QUALITIES
    placement: str          # left / right / center / adaptive
    matched: bool           # did the keeper cover the shot
    outcome: str            # goal / save / miss


def _weighted(rng: random.Random, weights: dict) -> str:
    items = list(weights.items())
    total = sum(w for _, w in items) or 1.0
    r = rng.random() * total
    for key, w in items:
        r -= w
        if r <= 0:
            return key
    return items[-1][0]


# ───────────────────────── shot selection ─────────────────────────

def select_shot_type(sh: PenaltyProfile, duel: DuelContext, rng: random.Random) -> str:
    p = sh.player
    w = {t: 1.0 for t in SHOT_TYPES}          # baseline
    # skills steer the intent
    w["instep_drive"] += 0.20 * p.scoring
    w["center_blast"] += 0.14 * p.scoring
    w["sidefoot"] += 0.18 * p.set_pieces
    w["curl"] += 0.14 * p.set_pieces
    w["wait_out_keeper"] += 0.16 * p.playmaking
    w["center_placement"] += 0.08 * p.playmaking
    # specialty
    if sh.specialty == "technical":
        w["curl"] += 4; w["panenka"] += 3; w["chip"] += 3
    elif sh.specialty == "powerful":
        w["instep_drive"] += 4; w["center_blast"] += 3
    elif sh.specialty == "quick":
        w["toe_poke"] += 4; w["instep_drive"] += 2
    elif sh.specialty == "unpredictable":
        for t in SHOT_TYPES:
            w[t] += rng.uniform(0, 6)
    # personality
    if p.aggressiveness >= 4:
        w["instep_drive"] += 3; w["center_blast"] += 2
    elif p.aggressiveness <= 1:
        w["sidefoot"] += 2; w["center_placement"] += 2
    if p.honesty >= 4:                          # honest -> few tricks
        w["panenka"] *= 0.3; w["wait_out_keeper"] *= 0.6
    elif p.honesty <= 1:                        # dishonest -> deception
        w["panenka"] += 2; w["wait_out_keeper"] += 2; w["chip"] += 1
    # weaker foot: avoid the fancy stuff if you can't trust the foot
    if duel.weaker_foot and sh.weak_foot_ability < 0.45:
        for t in ("panenka", "chip", "curl"):
            w[t] *= 0.25
        w["sidefoot"] += 2; w["center_placement"] += 2; w["toe_poke"] += 1
    return _weighted(rng, w)


def _placement(shot_type: str, rng: random.Random) -> str:
    if shot_type in _ADAPTIVE_SHOTS:
        return "adaptive"
    if shot_type in _CENTER_SHOTS:
        return "center"
    if shot_type == "toe_poke":
        return rng.choice(["left", "right", "center"])
    return rng.choice(["left", "right"])         # side shots


# ───────────────────────── keeper response ─────────────────────────

def select_keeper_response(
    kp: PenaltyProfile, sh: PenaltyProfile, duel: DuelContext,
    placement: str, shot_type: str, rng: random.Random, cfg: Config,
):
    """Return (response, matched). The keeper reads body language with an accuracy
    capped well below certainty, so a great keeper matters but never dominates."""
    p_read = min(cfg.keeper_read_cap,
                 cfg.keeper_read_base + cfg.keeper_read_slope * kp.keeper_reading)
    # four-point: a poor weak-foot shooter rarely threatens the corners
    central_bias = duel.weaker_foot and sh.weak_foot_ability < 0.35

    reads = rng.random() < p_read
    if shot_type in _ADAPTIVE_SHOTS:
        # wait_out beats committed divers; patience/reading neutralises it
        if reads or rng.random() < 0.35:
            response = rng.choice(["delay_then_dive", "read_shooter", "stay_central"])
        else:
            response = rng.choice(["dive_left", "dive_right", "gamble"])
        matched = response in ("stay_central", "delay_then_dive", "read_shooter")
        return response, matched

    if reads:
        covered = placement
        response = {"center": "stay_central", "left": "dive_left",
                    "right": "dive_right"}[placement]
        if rng.random() < 0.3:
            response = "read_shooter"   # same cover, different flavour
    elif central_bias and rng.random() < 0.6:
        response, covered = "stay_central", "center"
    else:
        response = rng.choice(["dive_left", "dive_right", "stay_central",
                               "gamble", "delay_then_dive"])
        covered = {
            "dive_left": "left", "dive_right": "right", "stay_central": "center",
            "gamble": rng.choice(["left", "right"]),
            "delay_then_dive": placement if rng.random() < 0.5
            else rng.choice(["left", "right", "center"]),
        }[response]
    return response, covered == placement


# ───────────────────────── shot quality ─────────────────────────

def generate_shot_quality(sh: PenaltyProfile, duel: DuelContext, rng: random.Random,
                          cfg: Config) -> str:
    dist = _DIST_WEAK if duel.weaker_foot else _DIST_STRONG
    # sample a base index
    r = rng.random()
    idx = 0
    cum = 0.0
    for i, pr in enumerate(dist):
        cum += pr
        if r <= cum:
            idx = i
            break
    else:
        idx = len(dist) - 1

    # class nudges the execution up or down — stars strike well far more often.
    # general_class lets any high-TSI player benefit; scoring rewards forwards most.
    base = sh.weak_foot_ability if duel.weaker_foot else sh.penalty_technique
    star = (
        0.45 * base
        + 0.18 * sh.general_class
        + 0.27 * (sh.player.scoring / 20.0)   # forwards rewarded most
        + 0.10 * (sh.player.form / 8.0)
    )
    idx += int(round((star - 0.40) * cfg.quality_star_gain))

    # fatigue and temperament
    over = max(0, duel.attempt_number - cfg.fatigue_after)
    if over and rng.random() < over * (1.0 - sh.fatigue_resistance) * 0.15:
        idx -= 1
    if rng.random() < 0.4 * sh.chaos:           # temperament adds variance both ways
        idx += rng.choice([-1, 1])

    idx = max(0, min(5, idx))
    return QUALITIES[idx]


# ───────────────────────── resolve + orchestrate ─────────────────────────

def resolve(quality: str, matched: bool, rng: random.Random) -> str:
    qi = QUALITIES.index(quality)
    if rng.random() < _P_MISS[qi]:
        return "miss"
    table = _P_GOAL_MATCHED if matched else _P_GOAL_UNMATCHED
    return "goal" if rng.random() < table[qi] else "save"


def simulate_penalty(sh: PenaltyProfile, kp: PenaltyProfile, duel: DuelContext,
                     cfg: Config, rng: random.Random) -> PenaltyResult:
    shot_type = select_shot_type(sh, duel, rng)
    placement = _placement(shot_type, rng)
    response, matched = select_keeper_response(kp, sh, duel, placement, shot_type, rng, cfg)
    quality = generate_shot_quality(sh, duel, rng, cfg)
    outcome = resolve(quality, matched, rng)
    return PenaltyResult(shot_type, response, quality, placement, matched, outcome)
