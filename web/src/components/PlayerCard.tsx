import type { Player } from "../engine/types";

const SKILL_LABELS: Record<string, string> = {
  keeper: "Målvakt", defending: "Försvar", playmaking: "Spelfördelning",
  winger: "Ytter", passing: "Passning", scoring: "Målskytte", set_pieces: "Fasta",
};

const POSITION_LABEL: Record<string, string> = {
  keeper: "Målvakt", defender: "Försvarare", wingback: "Ytterback",
  winger: "Ytter", playmaker: "Mittfältare", forward: "Anfallare",
  trainer: "Tränare", former: "F.d. spelare",
};

const fmtValue = (v: number) => v.toLocaleString("sv-SE").replace(/,/g, " ");

export function PlayerCard({ player, onClose }: { player: Player; onClose: () => void }) {
  return (
    <div className="panel" style={{ borderColor: "var(--accent)" }}>
      <div className="row" style={{ borderBottom: "1px solid var(--line)" }}>
        <b className="name">{player.nationality.flag} {player.name}</b>
        <button className="ghost" onClick={onClose}>Stäng</button>
      </div>
      <p className="sub">
        {POSITION_LABEL[player.best_position] ?? player.best_position}
        {" · "}{player.age} år
        {player.specialty ? ` · ${player.specialty}` : ""}
        {player.homegrown ? " · egen produkt" : ""}
      </p>
      <p className="sub" style={{ marginTop: -6 }}>
        TSI {fmtValue(player.tsi)} · {player.nationality.name}
        {" · "}{player.matches} matcher · {player.goals} mål
        {player.arrival_year ? ` · vid klubben sedan ${player.arrival_year}` : ""}
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
