"""Tunable knobs for the Penalty Engine v2 (see penalty.py).

Only the values the v2 engine actually reads live here. The decision-based engine
replaced the old flat additive-xG model, so the v1 knobs (base goal chance, xG
floor/ceiling, realization factors, weaker-foot xG penalties, …) have been removed
along with the dead probability.py module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Config:
    # --- v2: keeper read accuracy (capped so a great keeper never dominates) ---
    keeper_read_base: float = 0.12
    keeper_read_slope: float = 0.50
    keeper_read_cap: float = 0.66

    # --- v2: how strongly class shows in execution (higher = stars win more) ---
    quality_star_gain: float = 6.5

    # --- fatigue (matters only in long duels) ---
    fatigue_after: int = 3            # attempts before legs get heavy

    # --- game / presentation ---
    watch_from: int = 10              # start live commentary when this many remain
    max_turns: int = 100_000          # safety cap against pathological no-goal loops
    seed: int | None = None           # set for a reproducible game
