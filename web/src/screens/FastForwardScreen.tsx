import { useEffect, useState } from "react";
import * as engine from "../engine/pyodideEngine";
import type { FastForward } from "../engine/types";
import { PrickMeter } from "../components/PrickMeter";

// Screen 2: silently fast-forward through the warm-up, revealing the eliminations
// as a quick cascade (mirrors the CLI "dust settles" recap), then offer to watch.
export function FastForwardScreen(props: {
  game: number; team: string; onDone: () => void;
}) {
  const { game, team, onDone } = props;
  const [ff, setFf] = useState<FastForward | null>(null);
  const [shown, setShown] = useState(0);

  useEffect(() => {
    engine.simulateUntilWatch(game).then(setFf);
  }, [game]);

  // reveal eliminations one by one for a bit of drama
  useEffect(() => {
    if (!ff) return;
    if (shown >= ff.eliminations.length) return;
    const t = setTimeout(() => setShown((s) => s + 1), 110);
    return () => clearTimeout(t);
  }, [ff, shown]);

  if (!ff) return <div className="spinner">Spelar uppvärmningen...</div>;

  const done = shown >= ff.eliminations.length;

  return (
    <>
      <h2>{team} — dammet lägger sig</h2>
      <div className="panel">
        {ff.eliminations.slice(0, shown).map((e, i) => (
          <div key={i} className="ff-step">
            <span>💥 {e.name} ute</span>
            <b>{e.alive_after} kvar</b>
          </div>
        ))}
      </div>

      {done && (
        <>
          <h2>Kvar i leken ({ff.alive})</h2>
          <div className="panel">
            {ff.survivors.map((r) => (
              <div key={r.id} className={"row " + (r.role === "keeper" ? "keeper" : "")}>
                <span className="name">{r.role === "keeper" ? "🧤 " : ""}{r.name}</span>
                <PrickMeter prickar={r.prickar} />
              </div>
            ))}
          </div>
        </>
      )}

      <button className="primary" disabled={!done} onClick={onDone}>
        Se slutspelet live
      </button>
    </>
  );
}
