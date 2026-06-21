import { useEffect, useMemo, useRef, useState } from "react";
import * as engine from "../engine/pyodideEngine";
import type { LoadedSquad, Player, UiStrings } from "../engine/types";
import { PlayerCard } from "../components/PlayerCard";

// Set once we've auto-shown the sample squad, so it only happens on a fresh install.
const SEEN_EXAMPLE_KEY = "pk_seen_example";

// Defensive→attacking order used for sorting (labels come from the language pack).
const POSITION_ORDER = ["keeper", "defender", "wingback", "winger", "playmaker", "forward", "trainer", "former"];

type SortKey = "tsi" | "position" | "age" | "name" | "matches";
const SORT_KEYS: SortKey[] = ["tsi", "position", "age", "name", "matches"];

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
  ui: UiStrings;
  lang: string;
  onLang: (l: string) => void;
  squad: LoadedSquad | null;
  onSquad: (s: LoadedSquad) => void;
  onStart: (watchFrom: number, seed: number | null) => void;
}) {
  const { ui, lang, onLang, squad, onSquad, onStart } = props;
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
      setErr(ui.file_error + (ex as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function loadExample() {
    setBusy(true); setErr(null);
    try {
      onSquad(await engine.loadExample());
    } catch (ex) {
      setErr(ui.file_error + (ex as Error).message);
    } finally {
      setBusy(false);
    }
  }

  // On a fresh install, preload the sample squad once so first-time users land on
  // a populated list and can start a game immediately. Skipped after they've
  // dismissed/replaced it, and never overrides a squad they've already loaded.
  const autoTried = useRef(false);
  useEffect(() => {
    if (autoTried.current || squad) return;
    autoTried.current = true;
    if (localStorage.getItem(SEEN_EXAMPLE_KEY)) return;
    localStorage.setItem(SEEN_EXAMPLE_KEY, "1");
    loadExample();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <p className="sub">{ui.intro}</p>

      <div className="langrow">
        {["sv", "en"].map((l) => (
          <button key={l} className={"ghost" + (lang === l ? " active" : "")}
                  onClick={() => onLang(l)}>{l.toUpperCase()}</button>
        ))}
      </div>

      <div className="panel">
        {/* No `accept` filter: Android's file picker greys out .hrf (it has no
            registered MIME type), so we accept any file and validate on parse. */}
        <label className="ghost clickable" style={{ display: "block", textAlign: "center", padding: 14 }}>
          {busy ? "…" : ui.choose_file}
          <input type="file" hidden onChange={onFile} disabled={busy} />
        </label>
        <button className="ghost clickable" disabled={busy}
                style={{ display: "block", width: "100%", marginTop: 8 }}
                onClick={loadExample}>
          {ui.try_example}
        </button>
        {err && <p className="sub" style={{ color: "var(--miss)" }}>{err}</p>}
      </div>

      {squad && (
        <>
          <h2>{squad.team} — {squad.count} {ui.players_word}</h2>

          <div className="sortbar">
            <span className="tag">{ui.sort_label}</span>
            {SORT_KEYS.map((key) => (
              <button key={key}
                      className={"ghost" + (sort === key ? " active" : "")}
                      onClick={() => setSort(key)}>{ui.sort[key]}</button>
            ))}
          </div>

          <div className="panel">
            {sorted.map((p) => (
              <div key={p.id} className="player-row clickable" onClick={() => setSelected(p)}>
                <div className="player-row-top">
                  <span className="name">{p.nationality.flag} {p.name}</span>
                  <span className="value">{fmtValue(p.tsi)} {ui.tsi_word}</span>
                </div>
                <div className="player-row-meta">
                  {ui.positions[p.best_position] ?? p.best_position}
                  {" · "}{p.age} {ui.card.years}
                  {" · "}{p.matches} {ui.matches_word}
                  {" · "}{p.goals} {ui.goals_word}
                  {p.arrival_year ? ` · ${ui.since_word} ${p.arrival_year}` : ""}
                </div>
              </div>
            ))}
          </div>

          <div className="panel">
            <div className="row" style={{ borderBottom: "none" }}>
              <span className="name">{ui.watch_from}</span>
              <input type="number" min={2} max={squad.count} value={watchFrom}
                     onChange={(e) => setWatchFrom(Number(e.target.value))}
                     style={{ width: 64 }} />
              <span className="tag">{ui.remaining_word}</span>
            </div>
          </div>
        </>
      )}

      {selected && <PlayerCard ui={ui} player={selected} onClose={() => setSelected(null)} />}

      <button className="primary" disabled={!squad}
              onClick={() => onStart(watchFrom, null)}>
        {ui.start}
      </button>
    </>
  );
}
