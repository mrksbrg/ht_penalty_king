"""Drama generator (v2).

The result narrative is built from the football facts the engine produced — the
shot type tried, how the keeper guessed, and how well it was struck — not from a
probability number. The run-up (setup) is unchanged. All wording lives in the
language packs.
"""

from __future__ import annotations

import random

from .game import Event, GameResult
from .i18n import LANG
from .profiles import PenaltyProfile


def _name(result: GameResult, pid: int) -> str:
    return result.players[pid].name


def _pick(rng: random.Random, pool: list) -> str:
    return rng.choice(pool)


def is_big_moment(ev: Event) -> bool:
    return bool(
        ev.keeper_eliminated
        or ev.weaker_foot
        or ev.alive_before <= 3
        or ev.keeper_concede_streak >= 2
        or (ev.scored and ev.keeper_prickar_after == 4)
        or ev.quality in ("legendary", "catastrophic")
    )


def _ctx(ev: Event, sh: PenaltyProfile, kp: PenaltyProfile, result: GameResult) -> dict:
    p = sh.player
    best = max(p.keeper, p.defending, p.playmaking, p.winger,
               p.passing, p.scoring, p.set_pieces)
    return {
        "s": _name(result, ev.shooter_id),
        "k": _name(result, ev.keeper_id),
        "nk": _name(result, ev.new_keeper_id) if ev.new_keeper_id else "",
        "sal": f"{p.salary:,}".replace(",", " "),
        "ssp": LANG.skill(p.set_pieces),
        "ssc": LANG.skill(p.scoring),
        "sbest": LANG.skill(best),
        "kkeep": LANG.skill(kp.player.keeper),
    }


def _fmt(txt: str, ctx: dict, **extra) -> str:
    return txt.format(**ctx, **extra)


def _first_trait(traits: list, table: dict, rng: random.Random) -> str | None:
    hits = [t for t in traits if t in table]
    return rng.choice(hits) if hits else None


# ───────────────────────── run-up (unchanged) ─────────────────────────

def setup_text(ev: Event, sh: PenaltyProfile, kp: PenaltyProfile,
               result: GameResult, rng: random.Random) -> str:
    S = LANG.S
    ctx = _ctx(ev, sh, kp, result)
    if not is_big_moment(ev):
        return _fmt(_pick(rng, S["runup_neutral"]), ctx)

    lines: list[str] = []
    if ev.weaker_foot:
        lines.append(_fmt(_pick(rng, S["runup_situation"]["matchpoint"]), ctx))
    elif ev.alive_before <= 3:
        lines.append(_fmt(_pick(rng, S["runup_situation"]["final"]), ctx))
    elif ev.keeper_concede_streak >= 2:
        lines.append(_fmt(_pick(rng, S["runup_situation"]["siege"]), ctx))

    trait = _first_trait(sh.report_traits, S["runup_trait"], rng)
    if trait:
        lines.append(_fmt(_pick(rng, S["runup_trait"][trait]), ctx))
    else:
        lines.append(_fmt(_pick(rng, S["runup_neutral"]), ctx))
    return " ".join(lines)


# ───────────────────────── barbs (unchanged) ─────────────────────────

def _barb(ev: Event, sh: PenaltyProfile, ctx: dict, rng: random.Random) -> str:
    S = LANG.S["barb"]
    t = sh.report_traits
    keys = []
    if ev.scored:
        for key, trait in (("klassspelare_goal", "klassspelare"),
                           ("hopplos_goal", "hopplos"),
                           ("sympatisk_goal", "sympatisk"),
                           ("age_uråldrig_goal", "age_uråldrig"),
                           ("otrevlig", "otrevlig")):
            if trait in t and key in S:
                keys.append(key)
    else:
        for key, trait in (("dyrgrip_miss", "dyrgrip"),
                           ("trotjanare_miss", "trotjanare"),
                           ("nyforvarv_miss", "nyforvarv"),
                           ("temperamentsfull_miss", "temperamentsfull")):
            if trait in t and key in S:
                keys.append(key)
    if not keys:
        return ""
    return _fmt(_pick(rng, S[rng.choice(keys)]), ctx)


def _block(lines: list) -> str:
    return "\n".join(("   " + ln) if ln else "" for ln in lines)


def _opt(table: dict, key: str, ctx: dict, rng: random.Random) -> str:
    """Pick from table[key] if present, formatted; else ''."""
    pool = table.get(key)
    return _fmt(_pick(rng, pool), ctx) if pool else ""


def _aftermath(ev: Event, ctx: dict, rng: random.Random) -> str:
    """The line where the failed keeper leaves goal and the shooter takes over.
    Match point (weaker foot) draws from a 'survives' pool, otherwise 'escapes'."""
    key = "keeper_survives" if ev.weaker_foot else "keeper_escapes"
    return _fmt(_pick(rng, LANG.S[key]), ctx)


# ───────────────────────── result (v2) ─────────────────────────

def result_text(ev: Event, sh: PenaltyProfile, kp: PenaltyProfile,
                result: GameResult, rng: random.Random) -> str:
    S = LANG.S
    ui = S["ui"]
    ctx = _ctx(ev, sh, kp, result)
    big = is_big_moment(ev)

    attempt = _opt(S["shot_attempt"], ev.shot_type, ctx, rng)

    if ev.outcome == "goal":
        lines = ["", ui["banner_goal"], "", attempt]
        ex = _opt(S["exec_goal"], ev.quality, ctx, rng)
        if ex:
            lines.append(ex)
        if big:
            kb = _opt(S["keeper_beaten"], ev.keeper_response, ctx, rng)
            if kb:
                lines.append(kb)
        if ev.keeper_eliminated:
            lines.append(_fmt(ui["fifth_prick"], ctx))
            if ev.new_keeper_id is not None:
                lines.append(_fmt(ui["puts_on_gloves"], ctx))
        else:
            lines.append(_fmt(ui["prick_taken"], ctx, n=ev.keeper_prickar_after))

    elif ev.outcome == "save":
        lines = ["", ui["banner_save"], "", attempt]
        ks = _opt(S["keeper_save"], ev.keeper_response, ctx, rng)
        if ks:
            lines.append(ks)
        lines.append(_aftermath(ev, ctx, rng))

    else:  # miss
        lines = ["", ui["banner_miss"], "", attempt]
        em = _opt(S["exec_miss"], ev.quality, ctx, rng)
        if em:
            lines.append(em)
        lines.append(_aftermath(ev, ctx, rng))

    if big:
        barb = _barb(ev, sh, ctx, rng)
        if barb:
            lines.append(barb)
    return _block(lines)
