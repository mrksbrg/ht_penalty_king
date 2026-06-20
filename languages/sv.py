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
        # squad list: TSI, sorting, positions
        "tsi_word": "TSI",
        "sort_label": "Sortera:",
        "matches_word": "matcher",
        "since_word": "sedan",
        "sort": {
            "tsi": "TSI", "position": "Position", "age": "Ålder",
            "name": "Namn", "matches": "Matcher",
        },
        "positions": {
            "keeper": "Målvakt", "defender": "Försvarare", "wingback": "Ytterback",
            "winger": "Ytter", "playmaker": "Mittfältare", "forward": "Anfallare",
            "trainer": "Tränare", "former": "F.d. spelare",
        },
        # highscore (topplista)
        "highscore": "Topplista",
        "highscore_heading": "Topplista — flest vinster",
        "wins_word": "vinster",
        "wins_word_one": "vinst",
        "games_played": "spel",
        "games_played_one": "spel",
        "no_highscore": "Inga spel registrerade än. Spela ett parti först!",
        "back": "Tillbaka",
        "clear": "Rensa",
        "clear_confirm": "Rensa hela topplistan?",
        "export": "Exportera",
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
        "{s} mäter avståndet med blicken, som om det skulle ha ändrats sedan sist.",
        "{s} torkar händerna på byxorna och kliver fram. {k} väntar.",
        "{s} placerar bollen, backar tre steg och nickar för sig själv.",
        "Det blir {s} härnäst. {k} står kvar i buren med en min som talar sitt tydliga språk.",
        "{s} och {k}, gamla bekanta vid det här laget, gör upp igen.",
        "{s} kliver fram utan brådska. Ingen applåderar; det är ju bara träningen.",
        "{s} rättar till bollen en sista gång. {k} flyttar tyngden mellan fötterna.",
        "Ingen prestige på spel, säger alla. {s} ser inte ut att tro på det.",
        "{s} drar ett djupt andetag. {k}, {kkeep} mellan stolparna, gör likadant.",
        "{s} ställer upp bollen och låtsas att hela laget inte tittar.",
    ],
    "runup_trait": {
        "ledartyp": [
            "{s} går fram som om övningen redan tillhör honom.",
            "{s} tar plats vid bollen utan att fråga någon om lov.",
            "{s} pekar var bollen ska ligga, trots att det är uppenbart.",
            "{s} säger åt de andra att vara tysta. Det blir tyst.",
        ],
        "tystlaten": [
            "{s} ser lite obekväm ut med att alla tittar, trots att det bara är klubbkompisarna.",
            "{s} säger ingenting, gör ingen min, lägger bara bollen.",
            "{s} hade helst sluppit hela ögonblicket, det syns.",
        ],
        "otrevlig": [
            "{s} säger något kort till {k}. Knappast något vänligt.",
            "{s} skapar dålig stämning redan innan signalen.",
            "{s} möter {k}:s blick lite för länge för att det ska vara trevligt.",
            "{s} muttrar något om {k}:s handskar. Det var inte en komplimang.",
        ],
        "sympatisk": [
            "{s} ler nästan ursäktande redan på vägen fram.",
            "{s} klappar {k} på axeln först. Det lär inte hjälpa någon av dem.",
            "{s} säger något uppmuntrande till {k}, vilket är märkligt givet situationen.",
        ],
        "temperamentsfull": [
            "{s} ser irriterad ut, och det är fortfarande oklart på vad.",
            "{s} sparkar till en tuva innan han ens lagt bollen rätt.",
            "{s} muttrar för sig själv hela vägen fram.",
        ],
        "ohederlig": [
            "{s} börjar finta med kroppen innan han ens tagit sats.",
            "{s} sneglar åt ett håll så tydligt att det måste vara en bluff.",
            "{s} har redan bestämt sig för att luras. Frågan är bara hur.",
        ],
        "arlig": [
            "{s} gör ingen hemlighet av planen. Det blir en rak straff.",
            "{s} tittar precis dit han tänker skjuta. Ingen list i världen.",
            "{s} verkar fysiskt oförmögen att bluffa, och försöker inte.",
        ],
        "age_uråldrig": [
            "{s} inleder ansatsen som en man med två höfter.",
            "{s} tar sats med samma fart som han lämnar matsalen.",
            "{s} har gjort det här fler gånger än någon annan här varit född.",
        ],
        "age_junior": [
            "Ett stort ögonblick för {s}, som rakar sig ungefär en gång i veckan.",
            "{s} ser ut som om det här är hela hans säsong.",
            "Unge {s} försöker se cool ut. Det går sådär.",
        ],
        "dyrgrip": [
            "Det finns en {sbest} spelare någonstans i den kroppen. Frågan är om något av det tänker hjälpa till.",
            "{sal} kronor i veckan promenerar fram till pricken.",
            "{s} kostade en förmögenhet. Nu får vi se vad förmögenheten går för.",
        ],
        "trotjanare": [
            "{s} har burit klubbens färger länge nog för att veta hur länge det här kommer nämnas.",
            "{s} har stått här tusen gånger förut, på just den här planhalvan.",
            "{s} känner varje ojämnhet i gräset framför pricken vid det här laget.",
        ],
        "nyforvarv": [
            "Nyförvärvet {s} har inte varit här länge nog för att skratta bort en miss.",
            "{s} vill imponera. Det är aldrig ett bra utgångsläge på en straff.",
            "Ingen vet riktigt vad {s} går för än. Snart vet alla.",
        ],
    },
    "runup_situation": {
        "matchpoint": [
            "Matchboll. {k} står på fyra prickar — den här måste tas med fel fot.",
            "{k} är på brinkens kant. Fyra prickar. Svagare foten gäller.",
            "Fyra prickar på {k}. En till och leken är slut för honom. Och så — fel fot.",
            "Det är nu eller aldrig för {k}. Reglerna säger svagare foten, gräset säger lycka till.",
            "{s} får chansen att slå ut {k} — men måste göra det med den foten han helst glömmer.",
            "En straff från att åka ut. {k} håller andan. {s} byter fot.",
            "Matchboll mot {k}, och som om det inte vore nog: fel fot för {s}.",
            "Hela buren skälver. {k} på fyra, och {s} med fel fot på bollen.",
        ],
        "siege": [
            "{k} har redan släppt in flera i rad och börjar se ut att ångra hela leken.",
            "{k} har campat i buren ett tag nu, och inte frivilligt.",
            "Bollarna fortsätter trilla in bakom {k}. Det här börjar likna en belägring.",
            "{k} har inte fått lämna målet på evigheter och humöret därefter.",
            "Kö av skyttar, och {k} ensam kvar att svara för allihop. Igen.",
            "{k} ser ut som någon som glömt hur man tar sig ur en bur.",
            "Ännu en skytt fram mot en {k} som sett det mesta de senaste minuterna.",
        ],
        "final": [
            "Sista uppgörelsen. Det här avgör alltihop.",
            "Nere på de sista. Allt eller inget nu.",
            "Bara två kvar, och en av dem är på väg att förlora.",
            "Det här är vad hela leken kokat ner till. {s} mot {k}, inga fler ursäkter.",
            "Tystnaden är total. Det finns ingen kö kvar att gömma sig i.",
            "Slutduellen. Den som blinkar först bär skammen till nästa träning.",
            "Allt som hänt hittills var bara uppvärmning inför det här.",
        ],
    },

    # ───────── v2: vad skytten FÖRSÖKER (skotttyp) ─────────
    "shot_attempt": {
        "instep_drive": [
            "{s} tar lång ansats och går för ren kraft.",
            "{s} laddar för en riktig fullträff.",
            "{s} ska tydligen försöka spränga nätet.",
            "Lång ansats, axlarna tillbaka — {s} tänker dra på allt.",
            "{s} satsar inte på finess. Bara fart.",
            "{s} backar långt och siktar på att slå hål i målnätet.",
            "Inga konstigheter från {s}: spik och kraft.",
            "{s} ger sig på en vristspark som ska genom det mesta.",
        ],
        "sidefoot": [
            "{s} öppnar foten och siktar på placering.",
            "{s} satsar på precision i hörnet.",
            "{s} väljer säkerheten — bredsida mot stolproten.",
            "Lugnt och kontrollerat, {s} lägger an för en placerad straff.",
            "{s} struntar i kraften och litar på vinkeln.",
            "{s} vinklar foten och rullar an mot hörnet.",
            "Ren placering är planen för {s}. Inga muskler, bara mått.",
            "{s} sneglar mot hörnet och öppnar upp foten.",
        ],
        "curl": [
            "{s} lutar sig in och vill skruva den runt {k}.",
            "{s} försöker kröka in den i bortre hörnet.",
            "{s} lägger an för en skruv som ska runt {k}:s utsträckta hand.",
            "Insidan av foten, full skruv — {s} vill böja in den.",
            "{s} satsar på att låta bollen svänga in i bortre gaveln.",
            "{s} tänker kurva den, bort från {k} och in.",
            "En klassisk skruvstraff är på gång från {s}.",
            "{s} öppnar kroppen och försöker linda in den i krysset.",
        ],
        "panenka": [
            "{s} saktar in... det här blir en panenka.",
            "{s} bestämmer sig för fräckhet och chippar mot mitten.",
            "{s} håller emot till sista stund — det luktar panenka.",
            "Allas hjärtan stannar: {s} verkar gå på en panenka.",
            "{s} tar nästan paus i ansatsen. Det här blir fräckt eller pinsamt.",
            "{s} lyfter blicken, ler lite, och lägger an för en chip i mitten.",
            "Vågar han? {s} saktar farten — han vågar.",
            "{s} har bestämt sig för att förödmjuka någon. Panenka på gång.",
        ],
        "wait_out_keeper": [
            "{s} väntar, väntar — vill få {k} att röra sig först.",
            "{s} fryser till och stirrar ut {k}.",
            "{s} stannar mitt i ansatsen och väntar på {k}:s tålamod.",
            "Ett spel om nerver: {s} vägrar slå förrän {k} rört sig.",
            "{s} bromsar in och låter sekunderna göra jobbet åt honom.",
            "{s} pausar och utmanar {k} att hoppa först.",
            "Stillastående duell — {s} blinkar inte, väntar på {k}.",
            "{s} drar ut på det, helt avsiktligt, och iakttar {k}:s fötter.",
        ],
        "toe_poke": [
            "{s} stöter till den med tån, helt utan förvarning.",
            "Ingen ansats att tala om — {s} petar i väg den.",
            "{s} tånar iväg den innan {k} ens hunnit ställa sig.",
            "Fult men snabbt: {s} petar till bollen med tåspetsen.",
            "{s} hugger till med tån, helt utan elegans.",
            "Inget vackert — {s} stöter den med tåhättan och hoppas.",
            "{s} bestämmer sig sent och tånar iväg den.",
            "En ren tåsko från {s}, oväntat och ogudaktigt.",
        ],
        "chip": [
            "{s} försöker chippa den mjukt över {k}.",
            "{s} vill lyfta den lent över målvakten.",
            "{s} skär in foten under bollen för en mjuk lobb.",
            "{s} satsar på att vippa den över {k}:s händer.",
            "En len chip är planen — {s} vill se bollen dala in.",
            "{s} öppnar foten och försöker lyfta den över buren.",
            "{s} går för känsla och chippar mot ribbans insida.",
            "{s} vill att bollen ska sväva, inte fara. Chip på gång.",
        ],
        "center_blast": [
            "{s} laddar för en mittpiska rakt på {k}.",
            "{s} satsar allt på kraft genom mitten.",
            "{s} dunkar på rakt där {k} står — och hoppas han hoppat.",
            "Ingen vinkel, bara våld: {s} pucklar på mitt i mål.",
            "{s} spikar den centralt och litar på att {k} kastat sig.",
            "{s} kör rakt på, hårt och mitt i, allt eller inget.",
            "{s} smäller till den rakt fram. Ribban darrar redan.",
            "{s} väljer mitten och maximal kraft. Subtilt är det inte.",
        ],
        "center_placement": [
            "{s} satsar lugnt mitt i mål och hoppas {k} rör sig.",
            "{s} rullar lugnt mot mitten.",
            "{s} placerar den stilla i mitten, kallt och beräknande.",
            "Ingen kraft alls — {s} lägger den lugnt centralt.",
            "{s} litar på att {k} dyker, och rullar mot mitten.",
            "{s} väljer den enklaste vägen: rakt och stilla i mitten.",
            "{s} skjuter mjukt mot mitten och väntar sig att buren töms.",
            "Lugnt mittskott från {s}, helt utan stress.",
        ],
    },
    # ───────── v2: hur väl det utfördes (mål) ─────────
    "exec_goal": {
        "legendary": [
            "Utförandet är fulländat — fullständigt orädderbart.",
            "En perfekt träff. Ingen målvakt i världen tar den.",
            "Helt rent, helt omöjligt. Bollen slår i nät innan någon hinner reagera.",
            "Så slår man en straff. Punkt. Orörbart.",
            "Bollen går precis där den ska och lite till. Mästerligt.",
            "Träffen är så ren att till och med motståndarna ser imponerade ut.",
            "Det här är straffläggning som lärobok. Felfritt.",
        ],
        "excellent": [
            "Lysande träff, precis där den ska.",
            "Avslutet är förstklassigt.",
            "Riktigt välträffat — knappt en chans för {k}.",
            "Krispigt och precist. Bollen vet vart den ska.",
            "Mästerligt slaget, hårt och placerat.",
            "{k} sträcker sig, men det här var för bra.",
            "En förstklassig fullträff, inget att invända mot.",
        ],
        "good": [
            "Välträffat och tillräckligt.",
            "Rent och säkert.",
            "Stabilt slaget. Det räckte gott.",
            "Inget snack — ren träff, rätt riktning.",
            "Säkert avslut, aldrig riktigt i fara.",
            "Prydligt gjort. Bollen i nät utan dramatik.",
            "Kontrollerat och tryggt. Mål.",
        ],
        "average": [
            "Inte vackert, men det räcker.",
            "Halvdan träff — men in gick den.",
            "Ojämnt slaget, ändå över linjen.",
            "Inget för fotoalbumet, men målet räknas lika.",
            "En skarvig kontakt — och ändå mål.",
            "Sådär träffat, men {k} hann inte ändå.",
            "Mediokert slaget, men bollen hittade in.",
        ],
        "poor": [
            "Svagt slaget, men det smiter ändå in.",
            "Tafatt, nästan pinsamt — och ändå mål.",
            "Illa träffat, men {k} lyckas missa den ändå.",
            "Bollen studsar sig fram på något vis. Mål, otroligt nog.",
            "Knappt en straff att tala om, ändå i nät.",
            "Det borde inte ha gått in. Det gick in.",
            "Ynkligt slaget, lyckligt avslutat.",
        ],
    },
    # ───────── v2: hur väl det utfördes (miss) ─────────
    "exec_miss": {
        "catastrophic": [
            "Träffen blir fullständigt fel — en groda av sällan skådat slag.",
            "Helt fel på bollen. Den far någon helt annanstans än planerat.",
            "En ren luftträff. Någonstans skrattar en fotbollsgud.",
            "Bollen går i en riktning ingen, allra minst {s}, hade tänkt sig.",
            "Det där såg ut att göra ont mer på stoltheten än på foten.",
            "En sådan miss att även gräset ser generat ut.",
            "Fullständigt misträffat. Bollen lämnar planen helt på egen hand.",
        ],
        "poor": [
            "För illa slaget, och det går utanför.",
            "Tamt och snett — utanför.",
            "Svagt och fel, bollen letar sig utanför stolpen.",
            "Trög träff, fel riktning. Aldrig på mål.",
            "Slappt slaget och brett. Inget hot.",
            "Det rann av foten och fortsatte utanför.",
            "Halvhjärtat och snett. Utanför med marginal.",
        ],
        "average": [
            "Drar precis utanför stolpen.",
            "En tum för mycket. Utanför.",
            "Nära, men fel sida om stolpen.",
            "Bollen smiter förbi på utsidan. Suck.",
            "Millimeter fel, men fel är fel. Utanför.",
            "Skär precis bredvid. Så nära.",
            "En aning för brett — och {k} behövde inte lyfta ett finger.",
        ],
        "good": [
            "Välträffat men en hårsmån för brett.",
            "Bra slaget — men stolpen säger nej och ut.",
            "Hårt och precist, fast en centimeter åt fel håll.",
            "Perfekt kraft, otur med riktningen. Stolpen.",
            "Allt stämde utom det sista — i stolpen och ut.",
            "Förtjänade bättre, men ribban höll emot.",
            "Snyggt slaget rakt på järnet. Otur.",
        ],
    },
    # ───────── v2: målvaktens reaktion (mål) ─────────
    "keeper_beaten": {
        "stay_central": [
            "{k} stod kvar i mitten och kunde bara titta efter den.",
            "{k} gissade på mitten; bollen gick åt sidan.",
            "{k} blev stående och såg den segla förbi åt sidan.",
            "{k} höll mitten — bollen valde hörnet.",
            "{k} rörde sig inte, och det var precis fel beslut.",
        ],
        "dive_left": [
            "{k} kastade sig åt vänster — fel håll.",
            "{k} flög åt vänster medan bollen gick högerut.",
            "{k} valde vänster; bollen hade andra planer.",
            "{k} dök åt vänster och fick se den passera åt höger.",
            "{k} gick tidigt åt vänster och bollen tackade och gick höger.",
        ],
        "dive_right": [
            "{k} valde höger och valde fel.",
            "{k} dök åt höger; bollen var redan förbi åt andra hållet.",
            "{k} kastade sig höger medan bollen smet vänster.",
            "{k} gick åt höger. Bollen gick inte dit.",
            "{k} satsade på höger och fick fel sida.",
        ],
        "delay_then_dive": [
            "{k} väntade in den men kom ändå en aning sent.",
            "{k} läste den sent och nådde aldrig fram.",
            "{k} höll ut till sista stund, men inte tillräckligt.",
            "{k} avvaktade lite för länge och hann aldrig ner.",
            "{k} dröjde, dök, och var en bråkdel för sen.",
        ],
        "read_shooter": [
            "{k} läste rätt men nådde inte ända fram.",
            "{k} var på rätt sida — men inte i närheten av att nå den.",
            "{k} gissade rätt och blev ändå slagen av träffen.",
            "{k} hade rätt håll, fel räckvidd.",
            "{k} läste honom perfekt och kom ändå till korta.",
        ],
        "gamble": [
            "{k} chansade, och chansen sprack.",
            "{k} satsade allt åt ett håll och fick fel.",
            "{k} singlade slant i huvudet och förlorade.",
            "{k} tog en chansning som inte lönade sig.",
            "{k} kastade sig på vinst och vann ingenting.",
        ],
    },
    # ───────── v2: målvaktens reaktion (räddning) ─────────
    "keeper_save": {
        "stay_central": [
            "{k} stod kvar och svalde skottet mitt på.",
            "{k} blev stående i mitten — precis dit bollen kom.",
            "{k} höll nerverna, stannade kvar och tog den centralt.",
            "{k} rörde sig inte en tum och belönades med bollen i famnen.",
            "{k} läste mitten och svalde den utan att flytta fötterna.",
        ],
        "dive_left": [
            "{k} flög åt vänster och fick undan den.",
            "{k} kastade sig åt vänster och slog bort den.",
            "{k} dök vänster och fick en hand emellan.",
            "{k} kastade sig åt vänster precis i tid.",
            "{k} flög åt vänster och boxade den i säkerhet.",
        ],
        "dive_right": [
            "{k} kastade sig åt höger och slog undan den.",
            "{k} dök åt höger och plockade den.",
            "{k} gick åt höger och fick fingrarna på bollen.",
            "{k} flög höger och tryckte undan den.",
            "{k} dök åt höger och nådde precis fram.",
        ],
        "delay_then_dive": [
            "{k} väntade ut honom och plockade den sent.",
            "{k} höll sig kvar tills sista stund och tog den.",
            "{k} stod kvar längst av alla och vann nervkriget.",
            "{k} dröjde, läste den, och tog den i sista ögonblicket.",
            "{k} avvaktade perfekt och var där när bollen kom.",
        ],
        "read_shooter": [
            "{k} läste honom som en öppen bok och var på plats.",
            "{k} visste exakt vart den skulle. Räddning.",
            "{k} hade läst honom hela vägen och stod rätt.",
            "{k} listade ut planen i förväg och var redan där.",
            "{k} såg den komma långt innan {s} slog. Tryggt.",
        ],
        "gamble": [
            "{k} chansade — och fick rätt.",
            "{k} satsade åt ett håll och hade tur nog att ha rätt.",
            "{k} gissade vilt och gissade rätt.",
            "{k} tog en ren chansning som råkade gå hem.",
            "{k} kastade sig på måfå och fångade lyckan.",
        ],
    },

    # ───────── följdrad: målvakten slipper ur buren (räddning/miss) ─────────
    "keeper_escapes": [
        "{k} slipper äntligen ur buren. {s} får ta på sig handskarna.",
        "{k} är fri! {s} traskar surt mot målet.",
        "{k} kliver ut ur buren med ett leende. {s} byter plats med honom.",
        "Räddad — bokstavligen. {k} ut, {s} in i mål.",
        "{k} hade fått nog av buren, och nu är det {s}:s tur att lida.",
        "{k} slänger handskarna till {s} och försvinner in i kön.",
        "Pliktskyldigast tar {s} över handskarna medan {k} andas ut.",
        "{k} lämnar målet utan att se sig om. {s} ärver eländet.",
        "Ut ur buren går {k}, in i den kliver en föga road {s}.",
        "{k} är räddad ur fångenskapen. {s} får gå i fällan istället.",
    ],
    # ───────── följdrad: målvakten överlever matchboll (fel fot) ─────────
    "keeper_survives": [
        "{k} överlever — slipper buren OCH får leva. {s} måste i mål.",
        "{k} klarar matchbollen och slänger handskarna till {s}.",
        "Mot alla odds står {k} kvar i leken. {s} får ta över buren.",
        "{k} andas ut hela vägen ner till tårna. {s} in i mål istället.",
        "Räddad på fel fot — {k} lever vidare, {s} får handskarna.",
        "{k} smiter undan femte pricken med nöd och näppe. {s} tar över.",
        "{k} överlever det som såg omöjligt ut. {s} kliver surt in i buren.",
        "Inte idag, säger {k}, och lämnar målet till {s}.",
        "{k} klarar sig kvar — och {s} får betala för missen i mål.",
        "{k} lever, buren är ledig, och {s} har precis blivit dess nästa gäst.",
    ],

    # ───────── elaka avslutningsrader (stora ögonblick) ─────────
    "barb": {
        "dyrgrip_miss": [
            "{sal} kronor i veckan, och ändå slog han den som om bollen vore en faktura.",
            "För den lönen borde straffen ha kommit inramad. I stället kom den utanför.",
            "{sal} i veckan köper tydligen inte lugnet framför mål.",
        ],
        "trotjanare_miss": [
            "{s} har varit i klubben länge nog att veta exakt hur länge den här missen kommer nämnas.",
            "Trogen klubben i alla år, och ändå blir det här hans eftermäle på nästa fika.",
            "Lojaliteten räcker inte ända fram i dag. Det gjorde inte straffen heller.",
        ],
        "nyforvarv_miss": [
            "Nyförvärvet får inte den där sortens miss att försvinna med ett skratt.",
            "Välkommen till klubben. Det här är vad de kommer minnas av din första vecka.",
            "Inte riktigt den entré {s} hade hoppats på.",
        ],
        "klassspelare_goal": [
            "På pappret en {sbest} spelare. Inför mål blir han plötsligt mänsklig. Bollen gick ändå in.",
            "All den där klassen, och så löser han det med det enklaste tänkbara. Skönt för honom.",
            "En {sbest} spelare som äntligen lät det synas. Lite.",
        ],
        "hopplos_goal": [
            "Det fanns väldigt lite i den spelaren som tydde på det här. Och ändå.",
            "Ingen hade satt en krona på det. Bollen i nät ändå.",
            "Mot all logik och allt facit: mål.",
        ],
        "otrevlig": [
            "Han log inte efteråt. Det gjorde ingen annan heller.",
            "Ingen sträckte fram handen. Han hade inte heller velat ta den.",
            "Stämningen blev inte bättre av det här, och det visste han.",
        ],
        "sympatisk_goal": [
            "Han ber nästan om ursäkt för att han gjorde mål.",
            "Han firar med en blygsam nick, som om målet var en olägenhet.",
            "Till och med {k} får en uppmuntrande klapp. Otroligt.",
        ],
        "temperamentsfull_miss": [
            "Han stirrar på gräset som om gräset är personligt ansvarigt.",
            "Han sparkar till luften, sen till tuvan, sen till luften igen.",
            "Någon borde hålla sig undan honom de närmaste minuterna.",
        ],
        "age_uråldrig_goal": [
            "Det gick inte fort, men det gick listigt.",
            "Rutinen löste det som benen inte längre orkar.",
            "Gammal är äldst, åtminstone den här gången.",
        ],
    },

    # ───────── personlighet: skyttens reaktion på MÅL (varje mål) ─────────
    "trait_goal": {
        "ohederlig": [
            "{s} pekar mot skyn som om det var planerat hela tiden. Det var det inte.",
            "{s} firar lite för stort för att vara helt ärligt menat.",
            "{s} hävdar efteråt att han placerade den exakt där han sa. Ingen minns att han sa något.",
        ],
        "otrevlig": [
            "{s} firar rakt i ansiktet på {k}. Inte snyggt.",
            "{s} gör mål och ser till att alla vet det, högljutt.",
            "Inget lagfirande från {s} — bara en blick som säger 'self klart'.",
        ],
        "temperamentsfull": [
            "{s} vrålar ut målet som om det vore en cupfinal.",
            "{s} slår näven i luften så hårt att han nästan ramlar.",
            "{s} exploderar i jubel — det är ju bara träning, men ändå.",
        ],
        "sympatisk": [
            "{s} ber nästan {k} om ursäkt på vägen tillbaka.",
            "{s} firar diskret och klappar {k} uppmuntrande.",
            "{s} ser mest lättad ut, och ler ursäktande mot buren.",
        ],
        "arlig": [
            "{s} nickar kort, plockar bollen och går tillbaka. Inget mer med det.",
            "Ingen show från {s} — mål, och vidare.",
            "{s} firar ungefär som man kvitterar ett paket. Sakligt.",
        ],
        "lugn": [
            "{s} gör mål utan att en min förändras.",
            "{s} vänder och går tillbaka som om utgången aldrig var i fråga.",
            "Iskallt av {s}, som redan tänker på nästa sak.",
        ],
    },
    # ───────── personlighet: skyttens reaktion på MISS (varje miss) ─────────
    "trait_miss": {
        "ohederlig": [
            "{s} pekar genast på pricken, gräset, vinden — allt utom foten.",
            "{s} låtsas att något störde honom precis i ansatsen.",
            "{s} muttrar om att underlaget var manipulerat. Det var det inte.",
        ],
        "otrevlig": [
            "{s} sparkar till bollkorgen och skyller surt på {k}.",
            "{s} snäser åt den som vågar se road ut.",
            "{s} lämnar pricken utan ett ord, men med desto mer attityd.",
        ],
        "temperamentsfull": [
            "{s} får ett mindre utbrott och skriker mot ingenting särskilt.",
            "{s} slår ut med armarna och stirrar ilsket mot himlen.",
            "{s} ser ut att vilja sparka sönder målställningen.",
        ],
        "sympatisk": [
            "{s} ler generat och rycker urskuldande på axlarna.",
            "{s} ber nästan om ursäkt till laget för missen.",
            "{s} tar det med ett snällt litet 'oj' och går vidare.",
        ],
        "arlig": [
            "{s} pekar på sig själv. Helt mitt fel, säger gesten.",
            "{s} skakar på huvudet åt sig själv, inga ursäkter.",
            "{s} erkänner direkt att det var en usel straff.",
        ],
        "lugn": [
            "{s} rycker oberört på axlarna. Det händer.",
            "{s} ser inte ut att bry sig nämnvärt. Nästa.",
            "Inte en rynka i pannan på {s}, trots missen.",
        ],
    },
    # ───────── personlighet: målvaktens reaktion på RÄDDNING ─────────
    "keeper_save_trait": {
        "ohederlig": [
            "{k} hävdar att han läste skytten som en bok. Möjligen i efterhand.",
            "{k} firar som om han planerat varenda detalj.",
        ],
        "otrevlig": [
            "{k} ger skytten en hånfull applåd. Helt onödigt.",
            "{k} säger något kort och elakt åt skytten på väg upp.",
        ],
        "temperamentsfull": [
            "{k} vrålar ut räddningen rakt mot skytten.",
            "{k} pumpar nävarna som om han just vunnit allt.",
        ],
        "sympatisk": [
            "{k} hjälper nästan skytten på fötter efteråt.",
            "{k} ler ursäktande, som om räddningen var en olycka.",
        ],
        "arlig": [
            "{k} reser sig, nickar kort, säger inget. Bara en räddning.",
            "{k} firar inte ens — gick åt rätt håll, det var allt.",
        ],
        "lugn": [
            "{k} plockar bollen och ställer sig till rätta, helt oberörd.",
            "{k} räddar den som om det vore vardagsmat. Det är det kanske.",
        ],
    },
    # ───────── personlighet: kombinerade karaktärsporträtt (stora ögonblick) ─────────
    "archetype": {
        "villain": [
            "{s} är den sortens spelare man älskar att hata — och han njuter av rollen.",
            "Hela planen vet vad {s} är för typ. Otrevlig, opålitlig, och just nu mittpunkten.",
            "{s} skulle bua på sig själv om han stod på andra sidan. Skurken i pjäsen.",
        ],
        "loose_cannon": [
            "Ingen, allra minst {s} själv, vet vad som händer härnäst.",
            "{s} är en tändsticka i en bensinmack — spännande, livsfarlig, oberäknelig.",
            "Med {s} på pricken kan vad som helst hända, och brukar göra det.",
        ],
        "hothead": [
            "{s} har redan kokat över en gång i dag. Det här gör inte saken lugnare.",
            "Kort stubin, inga vänner kvar i kön — {s} spelar för sig själv.",
            "{s} ser ut att vilja slåss med någon, och bollen duger tills vidare.",
        ],
        "gentleman": [
            "{s}, lagets trevligaste man, gör det här med ett nästan generat leende.",
            "Om någon förtjänar ögonblicket är det {s}. Alla vet det, till och med {k}.",
            "{s} är så sympatisk att man nästan hejar på honom mot sin vilja.",
        ],
        "iceman": [
            "{s} har inte ändrat puls sedan uppvärmningen. Iskall, rakryggad.",
            "Det finns ingen press som biter på {s}. Han verkar närmast uttråkad.",
            "{s} gör det svåra till en rutinsak. Lugnet självt.",
        ],
        "trickster": [
            "{s} har redan en plan, och troligen en plan B som inte är helt ren.",
            "Kallhamrad och listig — {s} spelar mest schack medan de andra sparkar boll.",
            "{s} ler det där leendet som betyder att någon är på väg att luras.",
        ],
    },
}
