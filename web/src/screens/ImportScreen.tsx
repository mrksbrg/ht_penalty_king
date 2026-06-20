import { useState } from "react";
import * as engine from "../engine/pyodideEngine";
import type { LoadedSquad, Player } from "../engine/types";
import { PlayerCard } from "../components/PlayerCard";

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
  const [watchFrom, setWatchFrom] = useState(10);

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
          <div className="panel">
            {squad.players.map((p) => (
              <div key={p.id} className="row clickable" onClick={() => setSelected(p)}>
                <span className="name">{p.name}</span>
                <span className="tag">mål {p.skills.scoring} · mv {p.skills.keeper}</span>
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
