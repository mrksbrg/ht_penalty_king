"""Tunable knobs. The xG model is intentionally simple and additive so it stays
controllable: skills move the odds a fair bit, form/fatigue a little, and
personality / age / status mostly colour the *story* rather than the numbers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Config:
    # --- additive xG model (see probability.py) ---
    base_goal_chance: float = 0.76    # an average internal penalty
    shooter_bonus_lo: float = -0.18   # hopeless technique
    shooter_bonus_hi: float = 0.16    # world-class technique
    keeper_penalty_lo: float = -0.02  # an outfielder flapping in goal
    keeper_penalty_hi: float = -0.16  # a real keeper (never dominant)
    xg_floor: float = 0.38            # even a poor shot scores sometimes
    xg_ceil: float = 0.94             # even a great keeper is beaten sometimes

    # --- form as a 'realization' factor on technique / keeping ---
    realization_base: float = 0.78
    realization_form: float = 0.26
    realization_noise: float = 0.03

    # --- weaker foot (keeper on 4 prickar), scaled by Passing ---
    wf_xg_max: float = 0.18           # penalty for a passing-0 shooter
    wf_xg_min: float = 0.03           # penalty for a great passer

    # --- fatigue (matters only in long duels) ---
    fatigue_after: int = 3            # attempts before legs get heavy
    fatigue_scale: float = 0.02

    # --- chaos (temperament adds variance, both ways) ---
    chaos_swing: float = 0.06

    # --- v2: keeper read accuracy (capped so a great keeper never dominates) ---
    keeper_read_base: float = 0.12
    keeper_read_slope: float = 0.50
    keeper_read_cap: float = 0.66

    # --- v2: how strongly class shows in execution (higher = stars win more) ---
    quality_star_gain: float = 6.5

    # --- game / presentation ---
    watch_from: int = 10              # start live commentary when this many remain
    max_turns: int = 100_000          # safety cap against pathological no-goal loops
    seed: int | None = None           # set for a reproducible game
