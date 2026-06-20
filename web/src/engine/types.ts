// Shapes returned by the Python engine (engine.py serialisers). Kept in sync by
// hand; the engine is the source of truth.

export interface Skills {
  keeper: number; defending: number; playmaking: number; winger: number;
  passing: number; scoring: number; set_pieces: number;
}

export interface Nationality { id: number; name: string; flag: string }

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
