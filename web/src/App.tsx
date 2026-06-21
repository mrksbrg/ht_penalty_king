import { useEffect, useState } from "react";
import * as engine from "./engine/pyodideEngine";
import type { LoadedSquad, GameHandle, UiStrings } from "./engine/types";
import { ImportScreen } from "./screens/ImportScreen";
import { FastForwardScreen } from "./screens/FastForwardScreen";
import { WatchScreen } from "./screens/WatchScreen";
import { WinnerScreen } from "./screens/WinnerScreen";

type Phase = "boot" | "import" | "fastforward" | "watch" | "winner";

export function App() {
  const [phase, setPhase] = useState<Phase>("boot");
  const [status, setStatus] = useState("Startar...");
  const [squad, setSquad] = useState<LoadedSquad | null>(null);
  const [game, setGame] = useState<GameHandle | null>(null);
  const [lang, setLang] = useState("sv");
  const [ready, setReady] = useState(false);
  const [ui, setUi] = useState<UiStrings | null>(null);

  useEffect(() => {
    engine
      .initEngine(setStatus)
      .then(() => setReady(true))
      .catch((e) => setStatus("Fel vid start: " + e.message));
  }, []);

  // Apply the chosen language in the engine and pull the matching UI chrome.
  // Runs on first ready and on every language switch — this is what makes the
  // whole interface (not just the match commentary) react to the SV/EN toggle.
  useEffect(() => {
    if (!ready) return;
    let cancelled = false;
    (async () => {
      await engine.setLanguage(lang);
      const u = await engine.uiStrings();
      if (!cancelled) {
        setUi(u);
        setPhase((p) => (p === "boot" ? "import" : p));
      }
    })();
    return () => { cancelled = true; };
  }, [ready, lang]);

  async function startGame(watchFrom: number, seed: number | null) {
    if (!squad) return;
    await engine.setLanguage(lang);
    const g = await engine.createGame(squad.squad, seed, watchFrom);
    setGame(g);
    setPhase("fastforward");
  }

  return (
    <div className="app">
      <h1>PENALTY KING ⚽</h1>
      {(phase === "boot" || !ui) && <div className="spinner">{status}</div>}

      {phase === "import" && ui && (
        <ImportScreen
          ui={ui}
          lang={lang}
          onLang={setLang}
          squad={squad}
          onSquad={setSquad}
          onStart={startGame}
        />
      )}

      {phase === "fastforward" && game && squad && ui && (
        <FastForwardScreen
          ui={ui}
          game={game.game}
          team={squad.team}
          onDone={() => setPhase("watch")}
        />
      )}

      {phase === "watch" && game && ui && (
        <WatchScreen ui={ui} game={game.game} onFinished={() => setPhase("winner")} />
      )}

      {phase === "winner" && game && ui && (
        <WinnerScreen
          ui={ui}
          game={game.game}
          onReplay={() => {
            setGame(null);
            setPhase("import");
          }}
        />
      )}
    </div>
  );
}
