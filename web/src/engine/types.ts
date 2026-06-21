// Shapes returned by the Python engine (engine.py serialisers). Kept in sync by
// hand; the engine is the source of truth.

export interface Skills {
  keeper: number; defending: number; playmaking: number; winger: number;
  passing: number; scoring: number; set_pieces: number;
}

export interface Nationality { id: number; name: string; flag: string }

// The web UI chrome for the active language (engine.ui_strings() = STRINGS['web']).
export interface UiStrings {
  intro: string; choose_file: string; file_error: string;
  players_word: string; scoring_abbr: string; keeper_abbr: string;
  watch_from: string; remaining_word: string; start: string;
  warming_up: string; dust_settles: string; eliminated_word: string;
  no_eliminations: string; still_in: string; see_endgame: string;
  in_goal: string; shooting: string; in_queue: string;
  take_kick: string; next_shot: string; see_winner: string;
  outcome_goal: string; outcome_save: string; outcome_miss: string;
  last_standing: string; ranking_heading: string; stats_heading: string;
  prickar_word: string; goals_word: string; saves_word: string;
  survived_word: string; play_again: string; last_team: string;
  tsi_word: string; sort_label: string; matches_word: string; since_word: string;
  sort: Record<string, string>;
  positions: Record<string, string>;
  highscore: string; highscore_heading: string;
  wins_word: string; wins_word_one: string;
  games_played: string; games_played_one: string;
  no_highscore: string; back: string; clear: string; clear_confirm: string;
  export: string;
  card: { close: string; years: string; homegrown: string; skills: Record<string, string> };
}

export interface Player {
  id: number;
  name: string;
  age: number;
  skills: Skills;
  stamina: number; form: number; experience: number;
  leadership: number; loyalty: number;
  salary: number;
  tsi: number;                   // Hattrick TSI (the HRF 'mkt' field)
  best_position: string;         // key: keeper|defender|wingback|winger|playmaker|forward
  nationality: Nationality;
  goals: number;                 // goals for the current club
  arrival_year: number | null;   // year they joined the club
  specialty: string | null;
  personality: { agreeability: string; aggressiveness: string; honesty: string };
  homegrown: boolean; matches: number;
}

export interface LoadedSquad {
  squad: number;          // handle
  team: string;
  players: Player[];
  count: number;
}

export interface GameHandle {
  game: number;           // handle
  players: number;
  total_events: number;
  watch_from: number;
}

export interface Row {
  id: number; name: string; prickar: number; meter: string; role: string;
}

export interface FastForward {
  eliminations: { turn: number; name: string; alive_after: number }[];
  survivors: Row[];
  alive: number;
}

export interface CurrentShot {
  turn: number;
  alive: number;
  keeper: Row;
  shooter: Row;
  queue: Row[];
  weaker_foot: boolean;
  commentary: string;
}

export interface ShotResult {
  turn: number;
  outcome: "goal" | "save" | "miss";
  shot_type: string;
  quality: string;
  keeper_response: string;
  keeper: { id: number; name: string; prickar: number; meter: string };
  shooter: { id: number; name: string };
  keeper_eliminated: boolean;
  new_keeper: string | null;
  commentary: string;
  finished: boolean;
}

export interface RankRow { rank: number; id: number; name: string; prickar: number; }

export interface StatRow {
  id: number; name: string; goals: number; saves: number;
  kicks_in_goal: number; conceded: number;
  eliminations_survived: number; final_prickar: number;
}
