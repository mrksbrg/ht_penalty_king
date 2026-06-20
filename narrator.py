"""Presentation: the scoreboard (keeper + next shooter clearly flagged, then the
queue), recap and champion banner. Wording comes from the active language pack."""

from __future__ import annotations

import random

from .game import Event, GameResult
from .i18n import LANG
from . import report

PRICK = "●"
EMPTY = "○"
NAME_W = 22


def _name(result: GameResult, pid: int) -> str:
    return result.players[pid].name


def prick_meter(n: int) -> str:
    n = max(0, min(5, n))
    return PRICK * n + EMPTY * (5 - n)


def scoreboard(result: GameResult, ev: Event) -> str:
    ui = LANG.S["ui"]
    rows = ev.field_snapshot
    keeper = next(r for r in rows if r[2] == "keeper")
    shooter = next(r for r in rows if r[2] == "shooter")
    queue = [r for r in rows if r[2] == "queue"]

    def line(icon, pid, pr, tag=""):
        nm = _name(result, pid).ljust(NAME_W)
        suffix = f"   · {tag}" if tag else ""
        return f"{icon} {nm} {prick_meter(pr)}{suffix}"

    out = [ui["remaining"].format(n=ev.alive_before)]
    out.append(line("🧤", keeper[0], keeper[1], ui["in_goal_tag"]))
    out.append(line("⚽", shooter[0], shooter[1], ui["shooting_tag"]))
    out.append("")  # gap before the queue
    for pid, pr, _ in queue:
        out.append(line("  ", pid, pr))
    return "\n".join(out)


def narrate_setup(result: GameResult, ev: Event, rng: random.Random) -> str:
    sh = result.profiles[ev.shooter_id]
    kp = result.profiles[ev.keeper_id]
    return scoreboard(result, ev) + "\n\n" + report.setup_text(ev, sh, kp, result, rng)


def narrate_result(result: GameResult, ev: Event, rng: random.Random) -> str:
    sh = result.profiles[ev.shooter_id]
    kp = result.profiles[ev.keeper_id]
    return report.result_text(ev, sh, kp, result, rng)


def narrate_recap(result: GameResult, first_live: Event) -> str:
    ui = LANG.S["ui"]
    alive_ids = {pid for pid, _, _ in first_live.field_snapshot}
    out_so_far = [pid for pid in result.elimination_order if pid not in alive_ids]

    lines = ["", "═" * 56, "  " + ui["dust_settles"], "═" * 56]
    if out_so_far:
        names = ", ".join(_name(result, pid) for pid in out_so_far)
        lines.append(ui["already_out"].format(n=len(out_so_far), names=names))
    lines.append(ui["still_in"].format(n=first_live.alive_before))
    for pid, pr, role in first_live.field_snapshot:
        tag = "  " + ui["recap_in_goal"] if role == "keeper" else ""
        lines.append(f"     {_name(result, pid):<{NAME_W}} {prick_meter(pr)}{tag}")
    lines.append("═" * 56)
    lines.append(ui["live_from_here"])
    lines.append("")
    return "\n".join(lines)


def narrate_champion(result: GameResult) -> str:
    ui = LANG.S["ui"]
    champ = _name(result, result.winner)
    runner_up = (
        _name(result, result.elimination_order[-1])
        if result.elimination_order
        else "—"
    )
    return (
        "\n" + "🏆" * 18 + "\n"
        + ui["champion"].format(name=champ) + "\n"
        + ui["champion_sub"].format(n=len(result.elimination_order)) + "\n"
        + ui["champion_final"].format(runner=runner_up) + "\n"
        + ui["champion_tagline"] + "\n"
        + "🏆" * 18 + "\n"
    )
