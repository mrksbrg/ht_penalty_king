"""Public engine API — the single entry point that BOTH the CLI and the web app
use. No game logic lives here; this only wraps the existing engine (play_game in
game.py) and serialises its state into plain JSON-friendly data.

Design notes
------------
* Outcomes are produced solely by play_game(seed). The same HRF + seed therefore
  yields identical results in the terminal and in the browser — if they ever
  differ, that is a bug.
* The web UI holds only opaque integer *handles* and calls these functions; it
  never touches internal game state directly.
* Everything returned here is JSON-serialisable (ints, floats, str, bool, None,
  list, dict) so it crosses the Pyodide <-> JavaScript boundary cleanly.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from .config import Config
from .game import GameResult, play_game
from .hrf_parser import Player, parse_players, team_name
from .i18n import LANG
from . import report

# ── registries (handles keep JS away from internal objects) ──
_squads: dict[int, list[Player]] = {}
_sessions: dict[int, "GameSession"] = {}
_next = [1]


def _new_handle() -> int:
    h = _next[0]
    _next[0] += 1
    return h


# ── language ──
def set_language(code: str) -> None:
    LANG.use(code)


def available_languages() -> list[str]:
    from .languages import AVAILABLE
    return list(AVAILABLE)


def ui_strings() -> dict:
    """The web frontend's UI chrome for the active language (STRINGS['web'])."""
    return dict(LANG.S.get("web", {}))


# ── serialisation ──
def serialize_player(p: Player) -> dict:
    return {
        "id": p.pid,
        "name": p.name,
        "age": p.age_years,
        "skills": {
            "keeper": p.keeper, "defending": p.defending, "playmaking": p.playmaking,
            "winger": p.winger, "passing": p.passing, "scoring": p.scoring,
            "set_pieces": p.set_pieces,
        },
        "stamina": p.stamina, "form": p.form, "experience": p.experience,
        "leadership": p.leadership, "loyalty": p.loyalty,
        "salary": p.salary, "market_value": p.market_value,
        "specialty": p.speciality_label or None,
        "personality": {
            "agreeability": p.agreeability_label,
            "aggressiveness": p.aggressiveness_label,
            "honesty": p.honesty_label,
        },
        "homegrown": p.homegrown, "matches": p.matches_team,
    }


def _meter(n: int) -> str:
    n = max(0, min(5, n))
    return "●" * n + "○" * (5 - n)


def _row(session: "GameSession", pid: int, prickar: int, role: str) -> dict:
    return {"id": pid, "name": session.result.players[pid].name,
            "prickar": prickar, "meter": _meter(prickar), "role": role}


def _narr_rng(session: "GameSession", idx: int) -> random.Random:
    # deterministic per event, so commentary is stable across calls
    return random.Random((session.seed or 0) * 1000003 + idx + 1)


# ── loading ──
def load_hrf(path: str) -> dict:
    """Parse an HRF file already on disk (or written into the Pyodide FS)."""
    players = parse_players(path)
    h = _new_handle()
    _squads[h] = players
    return {
        "squad": h,
        "team": team_name(path),
        "players": [serialize_player(p) for p in players],
        "count": len(players),
    }


# ── session ──
@dataclass
class GameSession:
    result: GameResult
    watch_from: int
    seed: int | None
    cursor: int = 0


def create_game(squad: int, seed: int | None = None, watch_from: int = 10) -> dict:
    players = _squads[squad]
    cfg = Config(watch_from=watch_from, seed=seed)
    result = play_game(players, cfg, random.Random(seed))
    h = _new_handle()
    _sessions[h] = GameSession(result=result, watch_from=watch_from, seed=seed)
    return {
        "game": h,
        "players": len(players),
        "total_events": len(result.events),
        "watch_from": watch_from,
    }


def get_result(game: int) -> GameResult:
    """Python-only accessor (used by the rich CLI narrator)."""
    return _sessions[game].result


def _scoreboard(session: GameSession, ev) -> list:
    return [_row(session, pid, pr, role) for pid, pr, role in ev.field_snapshot]


def simulate_until_watch_threshold(game: int) -> dict:
    """Advance silently through the warm-up, returning the eliminations that
    happened and the survivors at the watch threshold (mirrors the CLI recap)."""
    s = _sessions[game]
    eliminations = []
    while s.cursor < len(s.result.events):
        ev = s.result.events[s.cursor]
        if ev.alive_before <= s.watch_from:
            break
        if ev.keeper_eliminated:
            eliminations.append({
                "turn": ev.turn,
                "name": s.result.players[ev.keeper_id].name,
                "alive_after": ev.alive_before - 1,
            })
        s.cursor += 1
    return {
        "eliminations": eliminations,
        "survivors": get_survivors(game),
        "alive": s.result.events[s.cursor].alive_before
        if s.cursor < len(s.result.events) else 1,
    }


def get_current_shot(game: int) -> dict | None:
    """The upcoming kick's setup (no outcome revealed, cursor not advanced)."""
    s = _sessions[game]
    if s.cursor >= len(s.result.events):
        return None
    ev = s.result.events[s.cursor]
    rng = _narr_rng(s, s.cursor)
    sh = s.result.profiles[ev.shooter_id]
    kp = s.result.profiles[ev.keeper_id]
    rows = _scoreboard(s, ev)
    return {
        "turn": ev.turn,
        "alive": ev.alive_before,
        "keeper": next(r for r in rows if r["role"] == "keeper"),
        "shooter": next(r for r in rows if r["role"] == "shooter"),
        "queue": [r for r in rows if r["role"] == "queue"],
        "weaker_foot": ev.weaker_foot,
        "commentary": report.setup_text(ev, sh, kp, s.result, rng),
    }


def advance_game(game: int) -> dict | None:
    """Resolve the current kick and advance one step. None when the game is over."""
    s = _sessions[game]
    if s.cursor >= len(s.result.events):
        return None
    ev = s.result.events[s.cursor]
    s.cursor += 1
    rng = _narr_rng(s, ev.turn + 500000)
    sh = s.result.profiles[ev.shooter_id]
    kp = s.result.profiles[ev.keeper_id]
    return {
        "turn": ev.turn,
        "outcome": ev.outcome,                 # goal / save / miss
        "shot_type": ev.shot_type,
        "quality": ev.quality,
        "keeper_response": ev.keeper_response,
        "keeper": {"id": ev.keeper_id, "name": s.result.players[ev.keeper_id].name,
                   "prickar": ev.keeper_prickar_after, "meter": _meter(ev.keeper_prickar_after)},
        "shooter": {"id": ev.shooter_id, "name": s.result.players[ev.shooter_id].name},
        "keeper_eliminated": ev.keeper_eliminated,
        "new_keeper": s.result.players[ev.new_keeper_id].name if ev.new_keeper_id else None,
        "commentary": report.result_text(ev, sh, kp, s.result, rng),
        "finished": s.cursor >= len(s.result.events),
    }


def get_survivors(game: int) -> list:
    """Players still alive as of the cursor (from the engine's own snapshots)."""
    s = _sessions[game]
    idx = min(s.cursor, len(s.result.events) - 1)
    if idx < 0:
        return []
    ev = s.result.events[idx]
    return [_row(s, pid, pr, role) for pid, pr, role in ev.field_snapshot]


def get_winner(game: int) -> dict | None:
    s = _sessions[game]
    if s.cursor < len(s.result.events):
        return None
    w = s.result.winner
    return {"id": w, "name": s.result.players[w].name}


def final_ranking(game: int) -> list:
    """1st = winner, then reverse elimination order (last eliminated = runner-up)."""
    s = _sessions[game]
    order = [s.result.winner] + list(reversed(s.result.elimination_order))
    return [{"rank": i + 1, "id": pid, "name": s.result.players[pid].name,
             "prickar": s.result.final_prickar[pid]} for i, pid in enumerate(order)]


def player_stats(game: int) -> list:
    """Per-player stats derived purely from the game's events."""
    s = _sessions[game]
    events = s.result.events
    pids = list(s.result.players.keys())
    stat = {pid: {"goals": 0, "saves": 0, "in_goal": 0, "conceded": 0} for pid in pids}
    for ev in events:
        if ev.outcome == "goal":
            stat[ev.shooter_id]["goals"] += 1
            stat[ev.keeper_id]["conceded"] += 1
        elif ev.outcome == "save":
            stat[ev.keeper_id]["saves"] += 1
        stat[ev.keeper_id]["in_goal"] += 1     # one kick faced
    elim_index = {pid: i for i, pid in enumerate(s.result.elimination_order)}
    n_elim = len(s.result.elimination_order)
    out = []
    for pid in pids:
        survived = n_elim - elim_index[pid] - 1 if pid in elim_index else n_elim
        out.append({
            "id": pid, "name": s.result.players[pid].name,
            "goals": stat[pid]["goals"], "saves": stat[pid]["saves"],
            "kicks_in_goal": stat[pid]["in_goal"], "conceded": stat[pid]["conceded"],
            "eliminations_survived": survived,
            "final_prickar": s.result.final_prickar[pid],
        })
    out.sort(key=lambda r: (-r["goals"], -r["saves"]))
    return out
