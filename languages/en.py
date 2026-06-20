# -*- coding: utf-8 -*-
"""English. Same keys as sv.py — translate the values, keep the keys.

Placeholders available in the penalty phrases:
    {s}  shooter name      {k}  keeper name      {nk} new keeper name
    {sal} shooter weekly salary
    {ssp} shooter Set Pieces level (Hattrick word)
    {ssc} shooter Scoring level
    {sbest} shooter's best skill (Hattrick word)
    {kkeep} keeper's Keeper level
"""

NAME = "English"

SKILL_LEVELS = [
    "non-existent", "disastrous", "wretched", "poor", "weak", "inadequate",
    "passable", "solid", "excellent", "formidable", "outstanding", "brilliant",
    "magnificent", "world class", "supernatural", "titanic", "extra-terrestrial",
    "mythical", "magical", "utopian", "divine",
]

STRINGS = {
    "ui": {
        "title": "PENALTY KING — {club}",
        "lineup": "{n} players line up.  Source: {file}",
        "seed": "(seed {seed})",
        "press_enter": "   ⚽ press Enter to take the kick... ",
        "remaining": "── {n} left ──",
        "in_goal_tag": "in goal",
        "shooting_tag": "shooting now",
        "banner_goal": "⚽   G O A L ! ! !",
        "banner_save": "🧤   S A V E D !",
        "banner_miss": "✗   M I S S !",
        "prick_taken": "{k} takes prick {n}/5.",
        "fifth_prick": "💥 Fifth prick — {k} is OUT!",
        "puts_on_gloves": "{nk} pulls on the gloves.",
        "keeper_escapes": "{k} finally escapes the goal. {s} has to go in.",
        "keeper_survives": "{k} survives — out of goal AND still alive. {s} must go in.",
        "dust_settles": "THE DUST SETTLES",
        "already_out": "  Already knocked out ({n}): {names}",
        "still_in": "  Still standing ({n}):",
        "recap_in_goal": "(in goal)",
        "live_from_here": "  Live from here — every kick counts.",
        "champion": "  CHAMPION: {name}!",
        "champion_sub": "  Last man standing — outlasted {n} rivals.",
        "champion_final": "  Won the final duel against {runner}.",
        "champion_tagline": "  This will be mentioned in the locker room longer than it deserves.",
    },

    "web": {
        "intro": "Import your Hattrick squad (.hrf) and play Fem Prickar.",
        "choose_file": "Choose HRF file",
        "file_error": "Couldn't read the file: ",
        "players_word": "players",
        "scoring_abbr": "gls",
        "keeper_abbr": "GK",
        "watch_from": "Show live from",
        "remaining_word": "left",
        "start": "Start the game",
        "warming_up": "Playing the warm-up...",
        "dust_settles": "The dust settles",
        "eliminated_word": "out",
        "no_eliminations": "No one out yet.",
        "still_in": "Still standing",
        "see_endgame": "Watch the endgame live",
        "in_goal": "in goal",
        "shooting": "shooting",
        "in_queue": "In the queue",
        "take_kick": "⚽ Take the kick",
        "next_shot": "Next kick",
        "see_winner": "See the winner 🏆",
        "outcome_goal": "GOAL",
        "outcome_save": "SAVE",
        "outcome_miss": "MISS",
        "last_standing": "Last man standing — Penalty King",
        "ranking_heading": "Ranking",
        "stats_heading": "Stats (most goals)",
        "prickar_word": "prickar",
        "goals_word": "goals",
        "saves_word": "saves",
        "survived_word": "survived",
        "play_again": "Play again",
        "last_team": "Last team",
        "card": {
            "close": "Close", "years": "yrs",
            "skills": {
                "keeper": "Keeper", "defending": "Defending", "playmaking": "Playmaking",
                "winger": "Winger", "passing": "Passing", "scoring": "Scoring",
                "set_pieces": "Set pieces", "form": "Form", "experience": "Experience",
            },
        },
    },

    "runup_neutral": [
        "{s} steps up against {k}, {kkeep} between the posts.",
        "{s} sets the ball down. {k} in goal — {kkeep} at that.",
        "{s} against {k}. Again.",
        "{s}, a {sbest} player on his best days, gets ready.",
    ],
    "runup_trait": {
        "ledartyp": [
            "{s} strides up as if the drill already belongs to him.",
            "{s} takes the ball without asking anyone's permission.",
        ],
        "tystlaten": [
            "{s} looks a little uneasy with everyone watching, even though it's only teammates.",
        ],
        "otrevlig": [
            "{s} says something short to {k}. Hardly friendly.",
            "{s} sours the mood before the whistle has even gone.",
        ],
        "sympatisk": [
            "{s} smiles almost apologetically on the way up.",
        ],
        "temperamentsfull": [
            "{s} looks annoyed, and it's still unclear at what.",
        ],
        "ohederlig": [
            "{s} starts feinting with his body before he's even taken a run-up.",
        ],
        "arlig": [
            "{s} makes no secret of the plan. This will be a straight penalty.",
        ],
        "age_uråldrig": [
            "{s} begins the run-up like a man with two hips.",
        ],
        "age_junior": [
            "A big moment for {s}, who shaves about once a week.",
        ],
        "dyrgrip": [
            "There's {sbest}-level talent somewhere in that body. Whether any of it helps is another matter.",
        ],
        "trotjanare": [
            "{s} has worn the club's colours long enough to know exactly how long this will get mentioned.",
        ],
        "nyforvarv": [
            "New signing {s} hasn't been here long enough to laugh off a miss.",
        ],
    },
    "runup_situation": {
        "matchpoint": [
            "Match point. {k} is on four prickar — this one must be taken on the weaker foot.",
            "{k} is on the brink. Four prickar. Weaker foot only.",
        ],
        "siege": [
            "{k} has already shipped several in a row and is starting to regret the whole game.",
            "{k} has been camped in goal a while now, and not by choice.",
        ],
        "final": [
            "The last showdown. This settles everything.",
            "Down to the last few. All or nothing now.",
        ],
    },

    "goal_style": {
        "panenka": [
            "He turns the penalty into a little art project and chips it down the middle.",
            "Dinked straight through the middle while the keeper has already dived. Cheeky.",
        ],
        "power": [
            "He hammers it into the top corner with pure power.",
            "Brutal strike. The keeper gets near it, but the ball has already decided.",
            "With his {ssc} Scoring he batters it in without mercy.",
        ],
        "placement": [
            "He places it low by the post, tidy and mean.",
            "With his {ssp} feel for set pieces he rolls it into the corner.",
        ],
        "angry": [
            "More fury than technique — but the ball didn't care.",
            "He strikes it as if the ball had insulted him personally. In it went.",
        ],
        "simple": [
            "No tricks. Three steps and a straight side-foot into the net.",
            "A provocatively honest penalty, straight down the middle.",
            "His {ssp} feel for set pieces didn't even need to show. Straight in.",
        ],
        "overcomplicated": [
            "Three body feints, a dramatic pause, and then into the far corner.",
            "He tried to fool everyone, possibly himself too. It went in anyway.",
        ],
        "quick": [
            "The run-up is over before the keeper has had time to be offended.",
        ],
        "head": [
            "He treats the penalty like an aerial duel, which is odd but effective.",
        ],
        "nervous": [
            "A shaky run-up, but the ball found its way in regardless.",
        ],
    },
    "goal_keeper": [
        "{k} dives the wrong way.",
        "{k} reads it right but can't get down in time.",
        "{k} gets fingertips to it, but no more.",
    ],

    "save_style": [
        "{k} goes the right way and beats it away.",
        "The dive comes early, the hand comes low, and the save is just good enough to be irritating.",
        "{k} reads him like an open book and plucks it out.",
        "{kkeep} keeping is just enough: {k} gathers it low.",
    ],
    "save_near": [
        "{k} gets an arm to it and steers it onto the post. Incredible.",
    ],
    "miss_style": [
        "The ball climbs over the bar and heads for the car park.",
        "Wide. Miles wide. {k} didn't even have to move.",
        "Off the post and out. The clang carries all the way to the locker room.",
        "So much for his {ssp} feel for set pieces — straight wide.",
    ],

    "barb": {
        "dyrgrip_miss": [
            "{sal} a week, and still he struck it like the ball was an invoice.",
        ],
        "trotjanare_miss": [
            "{s} has been at the club long enough to know exactly how long this miss will get mentioned.",
        ],
        "nyforvarv_miss": [
            "The new signing can't make that kind of miss vanish with a laugh.",
        ],
        "klassspelare_goal": [
            "On paper, {sbest}-level class. In front of goal he turns human. It went in anyway.",
        ],
        "hopplos_goal": [
            "There was very little in that player to suggest this. And yet.",
        ],
        "otrevlig": [
            "He didn't smile afterwards. Neither did anyone else.",
        ],
        "sympatisk_goal": [
            "He almost apologises for scoring.",
        ],
        "temperamentsfull_miss": [
            "He glares at the grass as if the grass were personally responsible.",
        ],
        "age_uråldrig_goal": [
            "It wasn't fast, but it was crafty.",
        ],
    },

    # ───────── v2: what the shooter TRIES (shot type) ─────────
    "shot_attempt": {
        "instep_drive": ["{s} takes a long run-up and goes for pure power.",
                         "{s} winds up for a proper screamer."],
        "sidefoot": ["{s} opens up the foot and aims for placement.",
                     "{s} goes for precision in the corner."],
        "curl": ["{s} leans in and tries to bend it around {k}.",
                 "{s} attempts to curl it into the far corner."],
        "panenka": ["{s} slows down... this is going to be a Panenka.",
                    "{s} decides on cheek and dinks it toward the middle."],
        "wait_out_keeper": ["{s} waits, and waits — wants {k} to move first.",
                            "{s} freezes and stares {k} down."],
        "toe_poke": ["{s} jabs at it with the toe, no warning at all.",
                     "No run-up to speak of — {s} pokes it away."],
        "chip": ["{s} tries to chip it softly over {k}.",
                 "{s} wants to lift it gently over the keeper."],
        "center_blast": ["{s} loads up a blast straight at {k}.",
                         "{s} bets everything on power through the middle."],
        "center_placement": ["{s} calmly aims down the middle, hoping {k} moves.",
                             "{s} rolls it calmly toward the centre."],
    },
    # ───────── v2: how well it was struck (goal) ─────────
    "exec_goal": {
        "legendary": ["The execution is flawless — utterly unsaveable.",
                      "A perfect strike. No keeper alive stops that."],
        "excellent": ["A brilliant strike, exactly where it should be.",
                      "The finish is first class."],
        "good": ["Well struck and enough.", "Clean and safe."],
        "average": ["Not pretty, but it does the job.",
                    "A scrappy contact — but in it went."],
        "poor": ["Weakly struck, but it sneaks in anyway.",
                 "Awkward, almost embarrassing — and still a goal."],
    },
    # ───────── v2: how well it was struck (miss) ─────────
    "exec_miss": {
        "catastrophic": ["The contact goes completely wrong — a howler for the ages.",
                         "All wrong on the ball. It flies somewhere other than intended.",
                         "A clean air-shot. Somewhere a football god is laughing."],
        "poor": ["Struck too badly, and it goes wide.",
                 "Tame and crooked — wide."],
        "average": ["Drags just wide of the post.", "An inch too much. Wide."],
        "good": ["Well struck but a hair too wide.",
                 "Good contact — but the post says no and out."],
    },
    # ───────── v2: keeper reaction (goal) ─────────
    "keeper_beaten": {
        "stay_central": ["{k} stayed central and could only watch it go.",
                         "{k} guessed the middle; the ball went to the side."],
        "dive_left": ["{k} dived left — wrong way.",
                      "{k} flew left while the ball went right."],
        "dive_right": ["{k} chose right and chose wrong.",
                       "{k} dived right; the ball was already past the other way."],
        "delay_then_dive": ["{k} waited for it but still got there a fraction late.",
                            "{k} read it late and never arrived."],
        "read_shooter": ["{k} read it right but couldn't quite reach.",
                         "{k} was on the right side — but nowhere near reaching it."],
        "gamble": ["{k} gambled, and the gamble failed.",
                   "{k} committed everything one way and got it wrong."],
    },
    # ───────── v2: keeper reaction (save) ─────────
    "keeper_save": {
        "stay_central": ["{k} stayed put and swallowed it down the middle.",
                         "{k} stood in the centre — exactly where it came."],
        "dive_left": ["{k} flew left and got it away.",
                      "{k} dived left and beat it clear."],
        "dive_right": ["{k} dived right and beat it away.",
                       "{k} went right and gathered it."],
        "delay_then_dive": ["{k} waited him out and took it late.",
                            "{k} held until the last instant and claimed it."],
        "read_shooter": ["{k} read him like an open book and was there.",
                         "{k} knew exactly where it was going. Saved."],
        "gamble": ["{k} gambled — and got it right.",
                   "{k} committed one way and was lucky enough to be right."],
    },
}
