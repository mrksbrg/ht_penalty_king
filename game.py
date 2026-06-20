"""The fem prickar state machine.

Rules (made precise):
  * One keeper, the rest queue up FIFO to shoot.
  * Goal  -> keeper gets a prick and STAYS in goal (under siege); the scorer struts
            to the back of the queue. A 5th prick eliminates the keeper and the front
            of the queue steps in (scoring never makes you keeper).
  * Save/miss -> the keeper ESCAPES to the back of the queue; the shooter who failed
            must go in goal. (Being keeper is the bad job; a save is your way out.)
  * Keeper on 4 prickar -> the shot must be taken on the weaker foot.
  * Last player un-eliminated wins.
"""

from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass, field

from .config import Config
from .hrf_parser import Player
from .penalty import DuelContext, simulate_penalty
from .profiles import PenaltyProfile, profile_cache


@dataclass
class Event:
    turn: int
    alive_before: int
    keeper_id: int
    shooter_id: int
    keeper_prickar_before: int
    weaker_foot: bool
    scored: bool
    outcome: str                   # "goal" / "save" / "miss"
    shot_type: str
    keeper_response: str
    quality: str
    matched: bool
    keeper_prickar_after: int
    keeper_eliminated: bool
    new_keeper_id: int | None
    keeper_concede_streak: int     # goals this keeper has shipped in a row, before now
    attempt_number: int            # kicks this keeper has faced this spell
    field_snapshot: list = field(default_factory=list)  # (pid, prickar, role)
    # role is one of: "keeper", "shooter" (the one taking this kick), "queue"


@dataclass
class GameResult:
    winner: int
    elimination_order: list
    final_prickar: dict
    events: list
    players: dict                  # pid -> Player
    profiles: dict                 # pid -> PenaltyProfile


def play_game(players: list[Player], cfg: Config, rng: random.Random) -> GameResult:
    by_id = {p.pid: p for p in players}
    profiles = profile_cache(players)
    ids = [p.pid for p in players]
    if len(ids) < 2:
        raise ValueError("Need at least 2 players to play.")

    rng.shuffle(ids)
    keeper = ids[0]
    queue = deque(ids[1:])
    prickar = {pid: 0 for pid in ids}
    alive = set(ids)
    elimination_order: list[int] = []
    events: list[Event] = []

    concede_streak = 0    # goals the current keeper has shipped in a row
    spell_attempts = 0    # kicks the current keeper has faced this spell

    turn = 0
    while len(alive) > 1 and turn < cfg.max_turns:
        turn += 1
        shooter = queue.popleft()
        prickar_before = prickar[keeper]
        weaker = prickar_before == 4
        spell_attempts += 1
        streak_before = concede_streak

        duel = DuelContext(
            attempt_number=spell_attempts,
            keeper_prickar=prickar_before,
            weaker_foot=weaker,
            alive=len(alive),
        )
        pen = simulate_penalty(profiles[shooter], profiles[keeper], duel, cfg, rng)
        scored = pen.outcome == "goal"

        snapshot = _snapshot(keeper, shooter, queue, prickar)
        keeper_eliminated = False
        old_keeper = keeper

        if scored:
            prickar[keeper] += 1
            concede_streak += 1
            if prickar[keeper] >= 5:
                keeper_eliminated = True
                alive.discard(keeper)
                elimination_order.append(keeper)
                if len(alive) > 1:
                    keeper = queue.popleft()       # front of line steps in
                    queue.append(shooter)          # scorer to the back
                else:
                    queue.append(shooter)
                    keeper = None                  # game over
                concede_streak = 0
                spell_attempts = 0
            else:
                queue.append(shooter)              # keeper stays, peppered
        else:
            queue.append(keeper)                   # keeper escapes to the queue
            keeper = shooter                       # the failed shooter goes in goal
            concede_streak = 0
            spell_attempts = 0

        events.append(
            Event(
                turn=turn,
                alive_before=len(snapshot),
                keeper_id=old_keeper,
                shooter_id=shooter,
                keeper_prickar_before=prickar_before,
                weaker_foot=weaker,
                scored=scored,
                outcome=pen.outcome,
                shot_type=pen.shot_type,
                keeper_response=pen.keeper_response,
                quality=pen.quality,
                matched=pen.matched,
                keeper_prickar_after=prickar[old_keeper],
                keeper_eliminated=keeper_eliminated,
                new_keeper_id=keeper,
                keeper_concede_streak=streak_before,
                attempt_number=duel.attempt_number,
                field_snapshot=snapshot,
            )
        )

    winner = next(iter(alive))
    return GameResult(
        winner=winner,
        elimination_order=elimination_order,
        final_prickar=prickar,
        events=events,
        players=by_id,
        profiles=profiles,
    )


def _snapshot(keeper: int, shooter: int, queue, prickar: dict[int, int]) -> list:
    """Ordered standings: keeper first, then the shooter taking this kick, then the
    rest of the queue in shooting order (front to back)."""
    rows = [(keeper, prickar[keeper], "keeper"), (shooter, prickar[shooter], "shooter")]
    rows += [(pid, prickar[pid], "queue") for pid in queue]
    return rows
