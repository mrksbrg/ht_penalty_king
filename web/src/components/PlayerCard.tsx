import type { Player } from "../engine/types";

const SKILL_LABELS: Record<string, string> = {
  keeper: "Målvakt", defending: "Försvar", playmaking: "Spelfördelning",
  winger: "Ytter", passing: "Passning", scoring: "Målskytte", set_pieces: "Fasta",
};

export function PlayerCard({ player, onClose }: { player: Player; onClose: () => void }) {
  return (
    <div className="panel" style={{ borderColor: "var(--accent)" }}>
      <div className="row" style={{ borderBottom: "1px solid var(--line)" }}>
        <b className="name">{player.name}</b>
        <button className="ghost" onClick={onClose}>Stäng</button>
      </div>
      <p className="sub">
        {player.age} år{player.specialty ? ` · ${player.specialty}` : ""}
        {player.homegrown ? " · egen produkt" : ""}
      </p>
      <div className="skillgrid">
        {Object.entries(player.skills).map(([k, v]) => (
          <div key={k}><span className="muted">{SKILL_LABELS[k] ?? k}</span><b>{v}</b></div>
        ))}
        <div><span className="muted">Form</span><b>{player.form}</b></div>
        <div><span className="muted">Rutin</span><b>{player.experience}</b></div>
      </div>
      <p className="sub" style={{ marginTop: 10 }}>
        {player.personality.aggressiveness} · {player.personality.agreeability} · {player.personality.honesty}
      </p>
    </div>
  );
}
