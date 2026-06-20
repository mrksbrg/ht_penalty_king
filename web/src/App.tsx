import { useEffect, useState } from "react";
import * as engine from "./engine/pyodideEngine";
import type { LoadedSquad, GameHandle } from "./engine/types";
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

  useEffect(() => {
    engine
      .initEngine(setStatus)
      .then(() => setPhase("import"))
      .catch((e) => setStatus("Fel vid start: " + e.message));
  }, []);

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
      {phase === "boot" && <div className="spinner">{status}</div>}

      {phase === "import" && (
        <ImportScreen
          lang={lang}
          onLang={setLang}
          squad={squad}
          onSquad={setSquad}
          onStart={startGame}
        />
      )}

      {phase === "fastforward" && game && squad && (
        <FastForwardScreen
          game={game.game}
          team={squad.team}
          onDone={() => setPhase("watch")}
        />
      )}

      {phase === "watch" && game && (
        <WatchScreen game={game.game} onFinished={() => setPhase("winner")} />
      )}

      {phase === "winner" && game && (
        <WinnerScreen
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
