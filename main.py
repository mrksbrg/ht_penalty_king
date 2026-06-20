"""Command-line entry point. Plays one watchable game by default.

Examples:
    python -m penalty_king                      # latest HRF, watch the final 10
    python -m penalty_king --watch-from 6       # only watch the final six
    python -m penalty_king --delay 1.5          # auto-play, 1.5s between shots
    python -m penalty_king --seed 42            # replay an identical game
    python -m penalty_king --stats 5000         # Monte Carlo win odds instead
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time

from .config import Config
from .hrf_parser import find_latest_hrf, parse_players, team_name
from .i18n import LANG
from .languages import AVAILABLE as LANGUAGES
from . import engine, narrator

# Default: the HO HRF folder next to this package's parent.
_DEFAULT_HRF_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "HO", "hrf"
)


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="penalty_king",
        description="Penalty King — Hattrick squad penalty shootout (the game 'fem prickar')."
    )
    ap.add_argument("--hrf", help="Path to a specific .hrf file.")
    ap.add_argument("--hrf-dir", default=_DEFAULT_HRF_DIR,
                    help="Folder of HRF files (newest is used).")
    ap.add_argument("--watch-from", type=int, default=10,
                    help="Start live commentary when this many players remain.")
    ap.add_argument("--delay", type=float, default=None,
                    help="Seconds between shots (auto-play). Omit to advance with Enter.")
    ap.add_argument("--seed", type=int, default=None,
                    help="Reproducible game. Omit for a fresh one.")
    ap.add_argument("--lang", choices=LANGUAGES, default="sv",
                    help="Commentary language (default: sv).")
    ap.add_argument("--stats", type=int, metavar="N", default=None,
                    help="Skip the show; run N Monte Carlo games and print win odds.")
    return ap


def _resolve_hrf(args) -> str:
    if args.hrf:
        return args.hrf
    return find_latest_hrf(args.hrf_dir)


def _advance(delay):
    if delay is None:
        try:
            input(LANG.ui("press_enter"))
        except EOFError:
            pass  # non-interactive: just roll on
    elif delay > 0:
        time.sleep(delay)


def _suspense(tense: bool) -> None:
    """A short 'ball in flight' beat between the kick and the reveal."""
    pause = 1.0 if tense else 0.45
    sys.stdout.write("   ⚽")
    sys.stdout.flush()
    for _ in range(3):
        time.sleep(pause / 3)
        sys.stdout.write(" .")
        sys.stdout.flush()
    print()


def _settle(ev) -> None:
    """Hold on the result so it's clearly readable before the next kick."""
    if ev.keeper_eliminated:
        time.sleep(2.2)      # an elimination deserves a beat
    elif ev.scored:
        time.sleep(1.5)
    else:
        time.sleep(1.3)


def run(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)
    LANG.use(args.lang)
    cfg = Config(watch_from=args.watch_from, seed=args.seed)

    try:
        hrf_path = _resolve_hrf(args)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.stats is not None:
        from .montecarlo import run_stats
        players = parse_players(hrf_path)
        club = team_name(hrf_path)
        print(f"{club} — {len(players)} players — {os.path.basename(hrf_path)}")
        print(run_stats(players, cfg, args.stats, seed=cfg.seed))
        return 0

    # Build the game through the shared engine API (same path the web app uses).
    loaded = engine.load_hrf(hrf_path)
    club = loaded["team"]
    g = engine.create_game(loaded["squad"], seed=cfg.seed, watch_from=cfg.watch_from)
    result = engine.get_result(g["game"])

    show_rng = random.Random(cfg.seed if cfg.seed is not None else random.random())
    print("\n" + LANG.ui("title", club=club))
    print(LANG.ui("lineup", n=loaded["count"], file=os.path.basename(hrf_path)))
    if cfg.seed is not None:
        print(LANG.ui("seed", seed=cfg.seed))

    live = False
    for ev in result.events:
        if not live and ev.alive_before <= cfg.watch_from:
            print(narrator.narrate_recap(result, ev))
            live = True
        if live:
            print(narrator.narrate_setup(result, ev, show_rng))
            _advance(args.delay)              # the click: now the kick is taken
            _suspense(ev.weaker_foot or ev.alive_before <= 3)  # ...ball in flight...
            print(narrator.narrate_result(result, ev, show_rng))
            print()
            _settle(ev)                       # let the result stand before moving on

    print(narrator.narrate_champion(result))
    return 0


def main():
    raise SystemExit(run())


if __name__ == "__main__":
    main()
