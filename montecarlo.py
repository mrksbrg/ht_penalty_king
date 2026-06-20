"""Optional extra: run many silent games and report win frequency. Not the main
event — the headline is the watchable single game in main.py."""

from __future__ import annotations

import random
from collections import Counter

from .config import Config
from .game import play_game
from .hrf_parser import Player


def run_stats(players: list[Player], cfg: Config, games: int, seed: int | None = None):
    wins: Counter[int] = Counter()
    finish_sum: dict[int, int] = {p.pid: 0 for p in players}
    n = len(players)
    base = random.Random(seed)

    for _ in range(games):
        rng = random.Random(base.random())
        result = play_game(players, cfg, rng)
        wins[result.winner] += 1
        # finishing position: winner = 1, last eliminated = 2, ...
        finish_sum[result.winner] += 1
        for place, pid in enumerate(reversed(result.elimination_order), start=2):
            finish_sum[pid] += place

    by_id = {p.pid: p for p in players}
    rows = []
    for p in players:
        rows.append(
            (
                p.name,
                wins[p.pid],
                100.0 * wins[p.pid] / games,
                finish_sum[p.pid] / games,
            )
        )
    rows.sort(key=lambda r: -r[1])

    out = ["", f"Monte Carlo — {games} games", "-" * 48,
           f"{'Player':<22}{'Wins':>6}{'Win %':>8}{'AvgPos':>8}"]
    for name, w, pct, avgpos in rows:
        out.append(f"{name:<22}{w:>6}{pct:>7.1f}%{avgpos:>8.1f}")
    return "\n".join(out)
