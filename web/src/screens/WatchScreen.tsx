import { useCallback, useEffect, useState } from "react";
import * as engine from "../engine/pyodideEngine";
import type { CurrentShot, ShotResult, UiStrings } from "../engine/types";
import { PrickMeter } from "../components/PrickMeter";

// Screen 3: one kick at a time. Show the run-up, tap to take the kick, reveal the
// result. The suspense lives on the button — exactly like the CLI.
export function WatchScreen(
  { ui, game, onFinished }: { ui: UiStrings; game: number; onFinished: () => void },
) {
  const [shot, setShot] = useState<CurrentShot | null>(null);
  const [result, setResult] = useState<ShotResult | null>(null);
  const [busy, setBusy] = useState(false);

  const loadNext = useCallback(async () => {
    const s = await engine.getCurrentShot(game);
    if (!s) { onFinished(); return; }
    setResult(null);
    setShot(s);
  }, [game, onFinished]);

  useEffect(() => { loadNext(); }, [loadNext]);

  async function takeKick() {
    setBusy(true);
    const r = await engine.advanceGame(game);
    setBusy(false);
    if (r) setResult(r);
  }

  if (!shot) return <div className="spinner">...</div>;

  return (
    <>
      <h2>{shot.alive} {ui.remaining_word}</h2>

      <div className="panel">
        <div className="row keeper">
          <span className="name">🧤 {shot.keeper.name}</span>
          <PrickMeter prickar={shot.keeper.prickar} />
          <span className="tag">{ui.in_goal}</span>
        </div>
        <div className="row shooter">
          <span className="name">⚽ {shot.shooter.name}</span>
          <PrickMeter prickar={shot.shooter.prickar} />
          <span className="tag">{ui.shooting}</span>
        </div>
      </div>

      {shot.queue.length > 0 && (
        <>
          <p className="sub" style={{ margin: "2px 2px 6px" }}>{ui.in_queue} ({shot.queue.length}):</p>
          <div className="panel">
            {shot.queue.map((q) => (
              <div key={q.id} className="row">
                <span className="name">{q.name}</span>
                <PrickMeter prickar={q.prickar} />
              </div>
            ))}
          </div>
        </>
      )}

      {!result && <p className="commentary">{shot.commentary}</p>}

      {result && (
        <div className="panel">
          <div className={"banner " + result.outcome}>
            {result.outcome === "goal" ? ui.outcome_goal
              : result.outcome === "save" ? ui.outcome_save : ui.outcome_miss}
          </div>
          <p className="commentary">{result.commentary}</p>
        </div>
      )}

      {!result ? (
        <button className="primary" disabled={busy} onClick={takeKick}>
          {busy ? "..." : ui.take_kick}
        </button>
      ) : result.finished ? (
        <button className="primary" onClick={onFinished}>{ui.see_winner}</button>
      ) : (
        <button className="primary" onClick={loadNext}>{ui.next_shot}</button>
      )}
    </>
  );
}
