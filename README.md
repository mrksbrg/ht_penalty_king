[![CodeScene Average Code Health](https://codescene.io/projects/81509/status-badges/average-code-health)](https://codescene.io/projects/81509)

# Penalty King

A spectator simulation of the Swedish schoolyard penalty game **"fem prickar"**,
played by your Hattrick squad straight from the latest HRF export.

One player is in goal; the rest queue up and take penalties. Score and the keeper
earns a *prick* and stays in goal under siege; miss or get saved and the keeper
escapes to the queue while *you* go in goal. Five prickar and you're out. Last
player standing wins. The game fast-forwards through the early rounds, then lets
you watch the final survivors fight it out shot by shot, with dry, club-internal
Swedish drama for every kick.

## Run it

From the `Hattrick Organizer` folder:

```bash
python -m penalty_king                 # newest HRF, watch the final 10, press Enter per shot
python -m penalty_king --watch-from 6  # only watch the final six
python -m penalty_king --delay 1.0     # auto-play, 1 second between shots
python -m penalty_king --seed 42       # replay an identical game
python -m penalty_king --stats 5000    # skip the show; print win odds instead
python -m penalty_king.tests.test_basic   # run the checks
```

### Options

| Flag | Meaning | Default |
|------|---------|---------|
| `--hrf PATH` | Use a specific HRF file | newest in `--hrf-dir` |
| `--hrf-dir DIR` | Folder of HRF files | `../HO/hrf` |
| `--watch-from N` | Start live commentary at N survivors | 10 |
| `--delay S` | Auto-play S seconds per shot (omit = press Enter) | Enter |
| `--seed N` | Reproducible game | random |
| `--lang sv\|en` | Commentary language | `sv` |
| `--stats N` | Monte Carlo: N silent games, print win % | off |

## Languages

All on-screen text lives in plain-text language packs under `languages/` — `sv.py`
(Swedish, default) and `en.py` (English). Each holds a `STRINGS` table and a
`SKILL_LEVELS` list of Hattrick denominations (`bra`, `fenomenal`, `utomjordisk`,
…) that the reports drop in to describe a player's ability. Run another language with
`--lang en`.

To **add** a language, copy `sv.py` to e.g. `de.py`, translate the values (keep the
keys), and run `--lang de`. To **refine** the wording, just edit the strings — no
code involved.

## How it works — Penalty Engine v2 (`penalty.py`)

Every player gets a **penalty profile** from their Hattrick attributes
(`profiles.py`). A kick is then simulated as a sequence of football decisions
rather than a single probability:

```
select shot type  →  keeper chooses a response  →  shot quality is generated
                  →  outcome resolved  →  narrative generated
```

1. **Shot type** — sidefoot, instep drive, curl, Panenka, wait-out, toe-poke,
   chip, centre blast, centre placement. The distribution follows the player
   (scoring → drives, set pieces → placement/curl, technical → Panenka/chip,
   personality and weaker foot shift it).
2. **Keeper response** — the keeper reads body language with accuracy *capped well
   below certainty* (so a great keeper matters but never dominates), and reacts to
   the expected shot, not the future.
3. **Shot quality** — catastrophic → legendary, on a strong- or weak-foot curve
   nudged by technique, form, fatigue and temperament. The same shot type can be a
   legendary placement or an air-shot.
4. **Outcome** — goal / save / miss, from whether the keeper covered the shot
   *times* how well it was struck. A perfect strike beats a keeper who guessed
   right; a mishit is saved easily.

This separation of *what is tried* from *how well it is executed* is what makes the
commentary varied. `generalClass` still separates a brilliant defender who can't
finish from a genuinely hopeless player. **Weaker foot** (keeper on four) lowers
quality and raises variance, scaled by a derived weak-foot ability — it doesn't
force a special shot type.

### The drama (`report.py`)

The reports are built from **tags**, not numbers — so every attribute can colour
the story even when it barely moves the odds. Form, experience, leadership,
loyalty, age, salary/market value, specialty and the three personality axes
(agreeable↔unpleasant, calm↔fiery, honest↔dishonest) all feed Swedish, dry,
faintly mean, locker-room-prestige commentary. Routine kicks get one line; big
moments (match point, eliminations, a keeper being peppered, the final few) get a
full 2–4 sentence report. Tune everything in `config.py`.

## Layout

```
fem_prickar/
├── config.py        # tunable xG knobs + pacing
├── hrf_parser.py    # find + parse newest HRF -> Player list (all drama fields)
├── profiles.py      # derive each player's penalty profile + report tags
├── penalty.py       # v2 engine: shot type → keeper read → quality → outcome
├── game.py          # the state machine -> GameResult
├── report.py        # tag-driven drama generator (language-agnostic logic)
├── narrator.py      # scoreboard, recap, champion banner
├── i18n.py          # active-language holder + skill-word lookup
├── languages/       # sv.py (default), en.py — editable string packs
├── montecarlo.py    # optional --stats win-odds mode
├── main.py          # CLI entry point + pacing
└── tests/           # invariant checks
```
