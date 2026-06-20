// Loads the authoritative Python engine into the browser via Pyodide and exposes
// a typed wrapper. React only ever calls these methods — it never touches game
// state. Because the actual Python play_game runs here, a given HRF + seed yields
// the SAME outcome as the CLI.

import { loadPyodide, type PyodideInterface } from "pyodide";
import type {
  LoadedSquad, GameHandle, FastForward, CurrentShot, ShotResult, Row, RankRow, StatRow,
} from "./types";

const PYODIDE_CDN = "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/";
const BASE = import.meta.env.BASE_URL || "/";

let pyodide: PyodideInterface | null = null;

async function fetchText(url: string): Promise<string> {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`failed to fetch ${url}: ${r.status}`);
  return r.text();
}

/** Boot Pyodide and load the engine package from /public/engine. */
export async function initEngine(
  onStatus?: (msg: string) => void,
): Promise<void> {
  if (pyodide) return;
  onStatus?.("Laddar Python-motorn...");
  pyodide = await loadPyodide({ indexURL: PYODIDE_CDN });

  onStatus?.("Hämtar spelmotorn...");
  const manifest: string[] = JSON.parse(await fetchText(`${BASE}engine/manifest.json`));

  const FS = pyodide.FS;
  const mkdirp = (dir: string) => {
    const parts = dir.split("/").filter(Boolean);
    let cur = "";
    for (const p of parts) {
      cur += "/" + p;
      try { FS.mkdir(cur); } catch { /* exists */ }
    }
  };
  mkdirp("/engine");

  for (const rel of manifest) {
    const dir = "/engine/" + rel.split("/").slice(0, -1).join("/");
    mkdirp(dir);
    const src = await fetchText(`${BASE}engine/${rel}`);
    FS.writeFile("/engine/" + rel, src);
  }

  onStatus?.("Startar motorn...");
  await pyodide.runPythonAsync(
    "import sys\n" +
    "if '/engine' not in sys.path: sys.path.insert(0, '/engine')\n" +
    "import ht_penalty_king.engine as eng\n",
  );
}

/** Run a Python expression and return its JSON-decoded value. */
async function call<T>(expr: string): Promise<T> {
  if (!pyodide) throw new Error("engine not initialised");
  const json = await pyodide.runPythonAsync(
    `import json; json.dumps(${expr}, default=str)`,
  );
  return JSON.parse(json) as T;
}

export function setLanguage(code: string): Promise<unknown> {
  return call(`eng.set_language(${JSON.stringify(code)}) or None`);
}

/** Parse an uploaded HRF file (its raw text) and return the squad. */
export async function loadHrf(text: string): Promise<LoadedSquad> {
  if (!pyodide) throw new Error("engine not initialised");
  try { pyodide.FS.mkdir("/uploads"); } catch { /* exists */ }
  pyodide.FS.writeFile("/uploads/team.hrf", text);
  return call<LoadedSquad>(`eng.load_hrf("/uploads/team.hrf")`);
}

export function createGame(
  squad: number, seed: number | null, watchFrom: number,
): Promise<GameHandle> {
  const seedExpr = seed === null ? "None" : String(seed | 0);
  return call<GameHandle>(`eng.create_game(${squad | 0}, ${seedExpr}, ${watchFrom | 0})`);
}

export const simulateUntilWatch = (g: number) =>
  call<FastForward>(`eng.simulate_until_watch_threshold(${g | 0})`);
export const getCurrentShot = (g: number) =>
  call<CurrentShot | null>(`eng.get_current_shot(${g | 0})`);
export const advanceGame = (g: number) =>
  call<ShotResult | null>(`eng.advance_game(${g | 0})`);
export const getSurvivors = (g: number) =>
  call<Row[]>(`eng.get_survivors(${g | 0})`);
export const getWinner = (g: number) =>
  call<{ id: number; name: string } | null>(`eng.get_winner(${g | 0})`);
export const finalRanking = (g: number) =>
  call<RankRow[]>(`eng.final_ranking(${g | 0})`);
export const playerStats = (g: number) =>
  call<StatRow[]>(`eng.player_stats(${g | 0})`);
