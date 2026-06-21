import { useEffect, useState } from "react";
import * as engine from "../engine/pyodideEngine";
import type { RankRow, StatRow, UiStrings } from "../engine/types";

// Screen 4: winner, final ranking and stats (all from game state via the engine).
export function WinnerScreen(
  { ui, game, onReplay }: { ui: UiStrings; game: number; onReplay: () => void },
) {
  const [ranking, setRanking] = useState<RankRow[]>([]);
  const [stats, setStats] = useState<StatRow[]>([]);
  const [tab, setTab] = useState<"ranking" | "stats">("ranking");

  useEffect(() => {
    engine.finalRanking(game).then(setRanking);
    engine.playerStats(game).then(setStats);
  }, [game]);

  const winner = ranking[0];

  return (
    <>
      <div className="center" style={{ margin: "20px 0" }}>
        <div className="big">🏆</div>
        <div className="big">{winner?.name ?? "..."}</div>
        <p className="sub">{ui.last_standing}</p>
      </div>

      <div className="langrow">
        <button className={"ghost" + (tab === "ranking" ? " active" : "")}
                onClick={() => setTab("ranking")}>{ui.ranking_heading}</button>
        <button className={"ghost" + (tab === "stats" ? " active" : "")}
                onClick={() => setTab("stats")}>{ui.stats_heading}</button>
      </div>

      {tab === "ranking" && (
        <div className="panel">
          {ranking.map((r) => (
            <div key={r.id} className="row">
              <span className="tag" style={{ width: 28 }}>{r.rank}.</span>
              <span className="name">{r.name}</span>
              <span className="tag">{r.prickar} {ui.prickar_word}</span>
            </div>
          ))}
        </div>
      )}

      {tab === "stats" && (
        <div className="panel">
          {stats.map((s) => (
            <div key={s.id} className="row">
              <span className="name">{s.name}</span>
              <span className="tag">
                {s.goals} {ui.goals_word} · {s.saves} {ui.saves_word} · {s.eliminations_survived} {ui.survived_word}
              </span>
            </div>
          ))}
        </div>
      )}

      <button className="primary" onClick={onReplay}>{ui.play_again}</button>
    </>
  );
}
