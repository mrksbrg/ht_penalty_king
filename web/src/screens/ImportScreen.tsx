import { useMemo, useState } from "react";
import * as engine from "../engine/pyodideEngine";
import type { LoadedSquad, Player } from "../engine/types";
import { PlayerCard } from "../components/PlayerCard";

// Swedish position labels + a defensive→attacking order used for sorting.
const POSITION_ORDER = ["keeper", "defender", "wingback", "winger", "playmaker", "forward", "trainer", "former"];
const POSITION_LABEL: Record<string, string> = {
  keeper: "Målvakt", defender: "Försvarare", wingback: "Ytterback",
  winger: "Ytter", playmaker: "Mittfältare", forward: "Anfallare",
  trainer: "Tränare", former: "F.d. spelare",
};

type SortKey = "tsi" | "position" | "age" | "name" | "matches";
const SORTS: { key: SortKey; label: string }[] = [
  { key: "tsi", label: "TSI" },
  { key: "position", label: "Position" },
  { key: "age", label: "Ålder" },
  { key: "name", label: "Namn" },
  { key: "matches", label: "Matcher" },
];

const fmtValue = (v: number) => v.toLocaleString("sv-SE").replace(/,/g, " ");

function sortPlayers(players: Player[], key: SortKey): Player[] {
  const out = [...players];
  switch (key) {
    case "name":
      return out.sort((a, b) => a.name.localeCompare(b.name, "sv"));
    case "age":
      return out.sort((a, b) => a.age - b.age || b.tsi - a.tsi);
    case "matches":
      return out.sort((a, b) => b.matches - a.matches || b.tsi - a.tsi);
    case "position":
      return out.sort(
        (a, b) =>
          POSITION_ORDER.indexOf(a.best_position) - POSITION_ORDER.indexOf(b.best_position) ||
          b.tsi - a.tsi,
      );
    case "tsi":
    default:
      return out.sort((a, b) => b.tsi - a.tsi);
  }
}

export function ImportScreen(props: {
  lang: string;
  onLang: (l: string) => void;
  squad: LoadedSquad | null;
  onSquad: (s: LoadedSquad) => void;
  onStart: (watchFrom: number, seed: number | null) => void;
}) {
  const { lang, onLang, squad, onSquad, onStart } = props;
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [selected, setSelected] = useState<Player | null>(null);
  const [watchFrom, setWatchFrom] = useState(5);
  const [sort, setSort] = useState<SortKey>("tsi");

  const sorted = useMemo(
    () => (squad ? sortPlayers(squad.players, sort) : []),
    [squad, sort],
  );

  async function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setBusy(true); setErr(null);
    try {
      const text = await file.text();
      const loaded = await engine.loadHrf(text);
      onSquad(loaded);
    } catch (ex) {
      setErr("Kunde inte läsa HRF-filen: " + (ex as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <p className="sub">Importera ditt Hattrick-lag och spela Fem Prickar.</p>

      <div className="langrow">
        {["sv", "en"].map((l) => (
          <button key={l} className={"ghost" + (lang === l ? " active" : "")}
                  onClick={() => onLang(l)}>{l.toUpperCase()}</button>
        ))}
      </div>

      <div className="panel">
        <label className="ghost clickable" style={{ display: "block", textAlign: "center", padding: 14 }}>
          {busy ? "Läser..." : "Välj HRF-fil"}
          <input type="file" accept=".hrf,text/plain" hidden onChange={onFile} disabled={busy} />
        </label>
        {err && <p className="sub" style={{ color: "var(--miss)" }}>{err}</p>}
      </div>

      {squad && (
        <>
          <h2>{squad.team} — {squad.count} spelare</h2>

          <div className="sortbar">
            <span className="tag">Sortera:</span>
            {SORTS.map((s) => (
              <button key={s.key}
                      className={"ghost" + (sort === s.key ? " active" : "")}
                      onClick={() => setSort(s.key)}>{s.label}</button>
            ))}
          </div>

          <div className="panel">
            {sorted.map((p) => (
              <div key={p.id} className="player-row clickable" onClick={() => setSelected(p)}>
                <div className="player-row-top">
                  <span className="name">{p.nationality.flag} {p.name}</span>
                  <span className="value">{fmtValue(p.tsi)} TSI</span>
                </div>
                <div className="player-row-meta">
                  {POSITION_LABEL[p.best_position] ?? p.best_position}
                  {" · "}{p.age} år
                  {" · "}{p.matches} matcher
                  {" · "}{p.goals} mål
                  {p.arrival_year ? ` · sedan ${p.arrival_year}` : ""}
                </div>
              </div>
            ))}
          </div>

          <div className="panel">
            <div className="row" style={{ borderBottom: "none" }}>
              <span className="name">Visa live från</span>
              <input type="number" min={2} max={squad.count} value={watchFrom}
                     onChange={(e) => setWatchFrom(Number(e.target.value))}
                     style={{ width: 64 }} />
              <span className="tag">kvar</span>
            </div>
          </div>
        </>
      )}

      {selected && <PlayerCard player={selected} onClose={() => setSelected(null)} />}

      <button className="primary" disabled={!squad}
              onClick={() => onStart(watchFrom, null)}>
        Starta spelet
      </button>
    </>
  );
}
