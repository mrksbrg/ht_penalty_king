"""Invariant checks (engine v2). Run with:
    python -m ht_penalty_king.tests.test_basic
"""

from __future__ import annotations

import os
import random
import string as _string

from ..config import Config
from ..game import play_game
from ..hrf_parser import Player, find_latest_hrf, parse_players
from ..penalty import DuelContext, QUALITIES, SHOT_TYPES, simulate_penalty
from ..profiles import derive_profile

# The bundled example HRF ships in the repo, so the real-file check always runs.
_HRF_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "example"
)

_DEFAULTS = dict(
    age_years=26, age_days=0, keeper=3, defending=4, playmaking=4, winger=3,
    passing=4, scoring=3, set_pieces=4, stamina=7, form=5, experience=4,
    leadership=5, loyalty=10, salary=30000, market_value=10000,
    goals_team=0, arrival_date="2023-01-01", country_id=1,
    speciality=0, speciality_label="", agreeability=2, agreeability_label="",
    aggressiveness=2, aggressiveness_label="", honesty=3, honesty_label="",
    warnings=0, homegrown=False, matches_team=50, injury=-1,
)


def mk(pid, name, **kw):
    d = dict(_DEFAULTS)
    d.update(kw)
    return Player(pid=pid, name=name, **d)


def _toy(n=12):
    return [mk(i, f"P{i}", keeper=(i % 5), passing=(i % 8), set_pieces=3 + (i % 4))
            for i in range(1, n + 1)]


def test_weak_foot_ability():
    pro = derive_profile(mk(1, "X", passing=14, winger=10, set_pieces=8))
    assert 0.0 <= pro.weak_foot_ability <= 1.0
    poor = derive_profile(mk(2, "Y", passing=1, winger=1, set_pieces=1, playmaking=1, scoring=1))
    assert pro.weak_foot_ability > poor.weak_foot_ability


def test_simulate_valid():
    cfg = Config()
    sh = derive_profile(mk(1, "S", set_pieces=8, scoring=7, passing=8))
    kp = derive_profile(mk(2, "K", keeper=10))
    duel = DuelContext(1, 0, False, 10)
    for s in range(300):
        r = simulate_penalty(sh, kp, duel, cfg, random.Random(s))
        assert r.outcome in ("goal", "save", "miss")
        assert r.shot_type in SHOT_TYPES
        assert r.quality in QUALITIES


def test_keeper_not_dominant():
    cfg = Config()
    sh = derive_profile(mk(1, "Avg", set_pieces=6, scoring=5, passing=6))
    elite = derive_profile(mk(2, "Elite", keeper=20, experience=12, playmaking=12))
    duel = DuelContext(1, 0, False, 10)
    goals = sum(1 for s in range(1500)
                if simulate_penalty(sh, elite, duel, cfg, random.Random(s)).outcome == "goal")
    rate = goals / 1500
    assert rate > 0.4, f"keeper too dominant: avg shot scores only {rate:.2f}"


# ──────────────────── language-pack safety tests ────────────────────

# Every placeholder in a narrative string must be one of these.
# report.py/_ctx() supplies them; anything else → KeyError at runtime.
_VALID_PLACEHOLDERS = {"s", "k", "nk", "sal", "ssp", "ssc", "sbest", "kkeep", "n"}

# These sections use different or no placeholders — skip them.
_SKIP_SECTIONS = {"web", "ui", "SKILL_LEVELS"}

# Pools picked unconditionally with rng.choice() — an empty list crashes.
_MANDATORY_POOLS = ("runup_neutral", "keeper_escapes", "keeper_survives")
# Dict pools whose every sub-list is also mandatory if the key exists.
_MANDATORY_DICTS = ("runup_trait", "runup_situation")


def _all_strings(obj):
    """Recursively yield every str leaf from a nested dict/list."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for item in obj:
            yield from _all_strings(item)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _all_strings(v)


def _placeholders(text: str) -> set[str]:
    """Extract bare field names from a Python format string."""
    return {
        fname.split(".")[0].split("[")[0]
        for _, fname, _, _ in _string.Formatter().parse(text)
        if fname is not None
    }


def test_language_placeholders():
    """No narrative string may reference an unknown placeholder."""
    from ..languages import sv, en
    for mod in (sv, en):
        narrative = {k: v for k, v in mod.STRINGS.items() if k not in _SKIP_SECTIONS}
        for text in _all_strings(narrative):
            bad = _placeholders(text) - _VALID_PLACEHOLDERS
            assert not bad, (
                f"[{mod.NAME}] unknown placeholder(s) {bad!r} in:\n  {text!r}"
            )


def test_language_mandatory_pools():
    """Pools that are always passed to rng.choice() must never be empty."""
    from ..languages import sv, en
    for mod in (sv, en):
        S = mod.STRINGS
        for key in _MANDATORY_POOLS:
            pool = S.get(key, [])
            assert pool, f"[{mod.NAME}] mandatory pool '{key}' is empty or missing"
        for dict_key in _MANDATORY_DICTS:
            for subkey, pool in S.get(dict_key, {}).items():
                assert pool, (
                    f"[{mod.NAME}] mandatory pool '{dict_key}[{subkey}]' is empty"
                )


def test_game_invariants():
    cfg = Config()
    players = _toy(12)
    for seed in range(40):
        r = play_game(players, cfg, random.Random(seed))
        alive = {p.pid for p in players} - set(r.elimination_order)
        assert len(alive) == 1 and r.winner in alive
        assert all(v <= 5 for v in r.final_prickar.values())
        for pid in r.elimination_order:
            assert r.final_prickar[pid] == 5


def _run_all():
    test_weak_foot_ability()
    test_simulate_valid()
    test_keeper_not_dominant()
    test_game_invariants()
    test_language_placeholders()
    test_language_mandatory_pools()
    if os.path.isdir(_HRF_DIR):
        players = parse_players(find_latest_hrf(_HRF_DIR))
        r = play_game(players, Config(seed=7), random.Random(7))
        assert r.winner in {p.pid for p in players}
        print(f"  real HRF ok: {len(players)} players, winner pid={r.winner}")
    print("All tests passed.")


if __name__ == "__main__":
    _run_all()
