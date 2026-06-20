# -*- coding: utf-8 -*-
"""Svenska (default). All speltext bor här — ändra fritt, det är ren text.

Platshållare som kan användas i straff-fraserna:
    {s}     skyttens namn          {k}     målvaktens namn
    {nk}    nya målvaktens namn     {sal}   skyttens veckolön
    {ssp}   skyttens nivå i fasta situationer (i hattrick-ord)
    {ssc}   skyttens nivå i målskytte
    {sbest} skyttens bästa färdighet (hattrick-ord)
    {kkeep} målvaktens nivå i målvaktsspel
"""

NAME = "Svenska"

# Hattrick-benämningar, index = färdighetsnivå (0..20). Justera om du vill.
SKILL_LEVELS = [
    "obefintlig",     # 0
    "katastrofal",    # 1
    "usel",           # 2
    "dålig",          # 3
    "hyfsad",         # 4
    "bra",            # 5
    "ypperlig",       # 6
    "enastående",     # 7
    "fenomenal",      # 8
    "unik",  	      # 9
    "legendarisk",    # 10
    "gudabenådad",    # 11
    "övernaturlig",   # 12
    "oförglömlig",    # 13
    "himmelsk",		  # 14
    "titanisk",       # 15
    "utomjordisk",    # 16
    "mytomspunnen",   # 17
    "magisk",         # 18
    "utopisk",        # 19
    "gudomlig",       # 20
]

STRINGS = {
    # ───────── gränssnitt ─────────
    "ui": {
        "title": "PENALTY KING — {club}",
        "lineup": "{n} spelare ställer upp.  Källa: {file}",
        "seed": "(seed {seed})",
        "press_enter": "   ⚽ tryck Enter för att lägga straffen... ",
        "remaining": "── {n} kvar ──",
        "in_goal_tag": "i mål",
        "shooting_tag": "skjuter nu",
        # resultatbanderoller — versaler och mellanrum så de syns direkt
        "banner_goal": "⚽   M Å L ! ! !",
        "banner_save": "🧤   R Ä D D N I N G !",
        "banner_miss": "✗   M I S S !",
        # följdrader
        "prick_taken": "{k} får prick {n}/5.",
        "fifth_prick": "💥 Femte pricken — {k} är UTE ur leken!",
        "puts_on_gloves": "{nk} tar på sig handskarna.",
        "keeper_escapes": "{k} slipper äntligen ur buren. {s} får ta på sig handskarna.",
        "keeper_survives": "{k} överlever — slipper buren OCH får leva. {s} måste i mål.",
        # recap
        "dust_settles": "DAMMET LÄGGER SIG",
        "already_out": "  Redan utslagna ({n}): {names}",
        "still_in": "  Kvar i leken ({n}):",
        "recap_in_goal": "(i mål)",
        "live_from_here": "  Live härifrån — varje straff räknas.",
        # mästare
        "champion": "  VINNARE: {name}!",
        "champion_sub": "  Sist kvar — överlevde {n} rivaler.",
        "champion_final": "  Sista duellen vanns mot {runner}.",
        "champion_tagline": "  Det här kommer nämnas i omklädningsrummet längre än det förtjänar.",
    },

    # ───────── webb-gränssnitt (play.html / React) ─────────
    "web": {
        "intro": "Importera ditt Hattrick-lag (.hrf) och spela Fem Prickar.",
        "choose_file": "Välj HRF-fil",
        "file_error": "Kunde inte läsa filen: ",
        "players_word": "spelare",
        "scoring_abbr": "mål",
        "keeper_abbr": "mv",
        "watch_from": "Visa live från",
        "remaining_word": "kvar",
        "start": "Starta spelet",
        "warming_up": "Spelar uppvärmningen...",
        "dust_settles": "Dammet lägger sig",
        "eliminated_word": "ute",
        "no_eliminations": "Inga utslagna ännu.",
        "still_in": "Kvar i leken",
        "see_endgame": "Se slutspelet live",
        "in_goal": "i mål",
        "shooting": "skjuter",
        "in_queue": "I kön",
        "take_kick": "⚽ Lägg straffen",
        "next_shot": "Nästa straff",
        "see_winner": "Se vinnaren 🏆",
        "outcome_goal": "MÅL",
        "outcome_save": "RÄDDNING",
        "outcome_miss": "MISS",
        "last_standing": "Sist kvar — Penalty King",
        "ranking_heading": "Placering",
        "stats_heading": "Statistik (flest mål)",
        "prickar_word": "prickar",
        "goals_word": "mål",
        "saves_word": "räddn.",
        "survived_word": "överlevda",
        "play_again": "Spela igen",
        "last_team": "Senaste lag",
        "card": {
            "close": "Stäng", "years": "år",
            "skills": {
                "keeper": "Målvakt", "defending": "Försvar", "playmaking": "Spelfördelning",
                "winger": "Ytter", "passing": "Passning", "scoring": "Målskytte",
                "set_pieces": "Fasta", "form": "Form", "experience": "Rutin",
            },
        },
    },

    # ───────── ansats (före skottet) ─────────
    "runup_neutral": [
        "{s} ställer sig till rätta mot {k}, {kkeep} mellan stolparna.",
        "{s} lägger bollen på pricken. {k} i mål — {kkeep} sådan.",
        "{s} mot {k}. Igen.",
        "{s}, en {sbest} spelare på sina bästa dagar, gör sig redo.",
    ],
    "runup_trait": {
        "ledartyp": [
            "{s} går fram som om övningen redan tillhör honom.",
            "{s} tar plats vid bollen utan att fråga någon om lov.",
        ],
        "tystlaten": [
            "{s} ser lite obekväm ut med att alla tittar, trots att det bara är klubbkompisarna.",
        ],
        "otrevlig": [
            "{s} säger något kort till {k}. Knappast något vänligt.",
            "{s} skapar dålig stämning redan innan signalen.",
        ],
        "sympatisk": [
            "{s} ler nästan ursäktande redan på vägen fram.",
        ],
        "temperamentsfull": [
            "{s} ser irriterad ut, och det är fortfarande oklart på vad.",
        ],
        "ohederlig": [
            "{s} börjar finta med kroppen innan han ens tagit sats.",
        ],
        "arlig": [
            "{s} gör ingen hemlighet av planen. Det blir en rak straff.",
        ],
        "age_uråldrig": [
            "{s} inleder ansatsen som en man med två höfter.",
        ],
        "age_junior": [
            "Ett stort ögonblick för {s}, som rakar sig ungefär en gång i veckan.",
        ],
        "dyrgrip": [
            "Det finns en {sbest} spelare någonstans i den kroppen. Frågan är om något av det tänker hjälpa till.",
        ],
        "trotjanare": [
            "{s} har burit klubbens färger länge nog för att veta hur länge det här kommer nämnas.",
        ],
        "nyforvarv": [
            "Nyförvärvet {s} har inte varit här länge nog för att skratta bort en miss.",
        ],
    },
    "runup_situation": {
        "matchpoint": [
            "Matchboll. {k} står på fyra prickar — den här måste tas med fel fot.",
            "{k} är på brinkens kant. Fyra prickar. Svagare foten gäller.",
        ],
        "siege": [
            "{k} har redan släppt in flera i rad och börjar se ut att ångra hela leken.",
            "{k} har campat i buren ett tag nu, och inte frivilligt.",
        ],
        "final": [
            "Sista uppgörelsen. Det här avgör alltihop.",
            "Nere på de sista. Allt eller inget nu.",
        ],
    },

    # ───────── mål ─────────
    "goal_style": {
        "panenka": [
            "Han gör straffen till ett litet konstprojekt och chippar in den i mitten.",
            "Lull-lull rakt genom mitten medan målvakten redan kastat sig. Fräckt.",
        ],
        "power": [
            "Han spikar den i krysset med ren kraft.",
            "Stenhårt avslut. Målvakten är på den, men bollen har redan bestämt sig.",
            "Med sitt {ssc} målskytte dunkar han in den utan nåd.",
        ],
        "placement": [
            "Han placerar den lågt vid stolpen, prydligt och elakt.",
            "Med sin {ssp} känsla för fasta situationer rullar han in den i hörnet.",
        ],
        "angry": [
            "Mer vrede än teknik — men bollen brydde sig inte.",
            "Han slår den som om bollen förolämpat honom personligen. In gick den.",
        ],
        "simple": [
            "Inga konster. Tre steg och en rak bredsida i mål.",
            "En provocerande ärlig straff, mitt i mål.",
            "Hans {ssp} känsla för fasta situationer behövde inte ens visa sig. Rakt in.",
        ],
        "overcomplicated": [
            "Tre kroppsfinter, en konstpaus, och sen in i bortre hörnet.",
            "Han försökte lura alla, möjligen även sig själv. Det gick ändå in.",
        ],
        "quick": [
            "Ansatsen är över innan målvakten hunnit bli förolämpad.",
        ],
        "head": [
            "Han behandlar straffen som en luftduell, vilket är märkligt men effektivt.",
        ],
        "nervous": [
            "Darrig ansats, men bollen letade sig in ändå.",
        ],
    },
    "goal_keeper": [
        "{k} kastar sig åt fel håll.",
        "{k} läser rätt men hinner inte ner.",
        "{k} får fingertopparna på den, men inte mer.",
    ],

    # ───────── räddning / miss ─────────
    "save_style": [
        "{k} går rätt och slår undan den.",
        "Kastet kommer tidigt, handen kommer lågt, och räddningen blir precis tillräckligt bra för att bli irriterande.",
        "{k} läser honom som en öppen bok och plockar den.",
        "{kkeep} målvaktsspel räcker precis: {k} fångar den lågt.",
    ],
    "save_near": [
        "{k} får en arm på den och styr den i stolpen. Otroligt.",
    ],
    "miss_style": [
        "Bollen stiger över ribban och fortsätter mot parkeringen.",
        "Utanför. Långt utanför. {k} behövde inte ens röra sig.",
        "I stolpen och ut. Plåtljudet hörs ända till omklädningsrummet.",
        "Så mycket för hans {ssp} känsla för fasta situationer — rakt utanför.",
    ],

    # ───────── elaka avslutningsrader (stora ögonblick) ─────────
    "barb": {
        "dyrgrip_miss": [
            "{sal} kronor i veckan, och ändå slog han den som om bollen vore en faktura.",
        ],
        "trotjanare_miss": [
            "{s} har varit i klubben länge nog att veta exakt hur länge den här missen kommer nämnas.",
        ],
        "nyforvarv_miss": [
            "Nyförvärvet får inte den där sortens miss att försvinna med ett skratt.",
        ],
        "klassspelare_goal": [
            "På pappret en {sbest} spelare. Inför mål blir han plötsligt mänsklig. Bollen gick ändå in.",
        ],
        "hopplos_goal": [
            "Det fanns väldigt lite i den spelaren som tydde på det här. Och ändå.",
        ],
        "otrevlig": [
            "Han log inte efteråt. Det gjorde ingen annan heller.",
        ],
        "sympatisk_goal": [
            "Han ber nästan om ursäkt för att han gjorde mål.",
        ],
        "temperamentsfull_miss": [
            "Han stirrar på gräset som om gräset är personligt ansvarigt.",
        ],
        "age_uråldrig_goal": [
            "Det gick inte fort, men det gick listigt.",
        ],
    },

    # ───────── v2: vad skytten FÖRSÖKER (skotttyp) ─────────
    "shot_attempt": {
        "instep_drive": ["{s} tar lång ansats och går för ren kraft.",
                         "{s} laddar för en riktig fullträff."],
        "sidefoot": ["{s} öppnar foten och siktar på placering.",
                     "{s} satsar på precision i hörnet."],
        "curl": ["{s} lutar sig in och vill skruva den runt {k}.",
                 "{s} försöker kröka in den i bortre hörnet."],
        "panenka": ["{s} saktar in... det här blir en panenka.",
                    "{s} bestämmer sig för fräckhet och chippar mot mitten."],
        "wait_out_keeper": ["{s} väntar, väntar — vill få {k} att röra sig först.",
                            "{s} fryser till och stirrar ut {k}."],
        "toe_poke": ["{s} stöter till den med tån, helt utan förvarning.",
                     "Ingen ansats att tala om — {s} petar i väg den."],
        "chip": ["{s} försöker chippa den mjukt över {k}.",
                 "{s} vill lyfta den lent över målvakten."],
        "center_blast": ["{s} laddar för en mittpiska rakt på {k}.",
                         "{s} satsar allt på kraft genom mitten."],
        "center_placement": ["{s} satsar lugnt mitt i mål och hoppas {k} rör sig.",
                             "{s} rullar lugnt mot mitten."],
    },
    # ───────── v2: hur väl det utfördes (mål) ─────────
    "exec_goal": {
        "legendary": ["Utförandet är fulländat — fullständigt orädderbart.",
                      "En perfekt träff. Ingen målvakt i världen tar den."],
        "excellent": ["Lysande träff, precis där den ska.",
                      "Avslutet är förstklassigt."],
        "good": ["Välträffat och tillräckligt.", "Rent och säkert."],
        "average": ["Inte vackert, men det räcker.",
                    "Halvdan träff — men in gick den."],
        "poor": ["Svagt slaget, men det smiter ändå in.",
                 "Tafatt, nästan pinsamt — och ändå mål."],
    },
    # ───────── v2: hur väl det utfördes (miss) ─────────
    "exec_miss": {
        "catastrophic": ["Träffen blir fullständigt fel — en groda av sällan skådat slag.",
                         "Helt fel på bollen. Den far någon helt annanstans än planerat.",
                         "En ren luftträff. Någonstans skrattar en fotbollsgud."],
        "poor": ["För illa slaget, och det går utanför.",
                 "Tamt och snett — utanför."],
        "average": ["Drar precis utanför stolpen.", "En tum för mycket. Utanför."],
        "good": ["Välträffat men en hårsmån för brett.",
                 "Bra slaget — men stolpen säger nej och ut."],
    },
    # ───────── v2: målvaktens reaktion (mål) ─────────
    "keeper_beaten": {
        "stay_central": ["{k} stod kvar i mitten och kunde bara titta efter den.",
                         "{k} gissade på mitten; bollen gick åt sidan."],
        "dive_left": ["{k} kastade sig åt vänster — fel håll.",
                      "{k} flög åt vänster medan bollen gick högerut."],
        "dive_right": ["{k} valde höger och valde fel.",
                       "{k} dök åt höger; bollen var redan förbi åt andra hållet."],
        "delay_then_dive": ["{k} väntade in den men kom ändå en aning sent.",
                            "{k} läste den sent och nådde aldrig fram."],
        "read_shooter": ["{k} läste rätt men nådde inte ända fram.",
                         "{k} var på rätt sida — men inte i närheten av att nå den."],
        "gamble": ["{k} chansade, och chansen sprack.",
                   "{k} satsade allt åt ett håll och fick fel."],
    },
    # ───────── v2: målvaktens reaktion (räddning) ─────────
    "keeper_save": {
        "stay_central": ["{k} stod kvar och svalde skottet mitt på.",
                         "{k} blev stående i mitten — precis dit bollen kom."],
        "dive_left": ["{k} flög åt vänster och fick undan den.",
                      "{k} kastade sig åt vänster och slog bort den."],
        "dive_right": ["{k} kastade sig åt höger och slog undan den.",
                       "{k} dök åt höger och plockade den."],
        "delay_then_dive": ["{k} väntade ut honom och plockade den sent.",
                            "{k} höll sig kvar tills sista stund och tog den."],
        "read_shooter": ["{k} läste honom som en öppen bok och var på plats.",
                         "{k} visste exakt vart den skulle. Räddning."],
        "gamble": ["{k} chansade — och fick rätt.",
                   "{k} satsade åt ett håll och hade tur nog att ha rätt."],
    },
}
