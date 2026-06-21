import type { Player, UiStrings } from "../engine/types";

const fmtValue = (v: number) => v.toLocaleString("sv-SE").replace(/,/g, " ");

export function PlayerCard(
  { ui, player, onClose }: { ui: UiStrings; player: Player; onClose: () => void },
) {
  const skills = ui.card.skills;
  return (
    <div className="panel" style={{ borderColor: "var(--accent)" }}>
      <div className="row" style={{ borderBottom: "1px solid var(--line)" }}>
        <b className="name">{player.nationality.flag} {player.name}</b>
        <button className="ghost" onClick={onClose}>{ui.card.close}</button>
      </div>
      <p className="sub">
        {ui.positions[player.best_position] ?? player.best_position}
        {" · "}{player.age} {ui.card.years}
        {player.specialty ? ` · ${player.specialty}` : ""}
        {player.homegrown ? ` · ${ui.card.homegrown}` : ""}
      </p>
      <p className="sub" style={{ marginTop: -6 }}>
        {ui.tsi_word} {fmtValue(player.tsi)} · {player.nationality.name}
        {" · "}{player.matches} {ui.matches_word} · {player.goals} {ui.goals_word}
        {player.arrival_year ? ` · ${ui.since_word} ${player.arrival_year}` : ""}
      </p>
      <div className="skillgrid">
        {Object.entries(player.skills).map(([k, v]) => (
          <div key={k}><span className="muted">{skills[k] ?? k}</span><b>{v}</b></div>
        ))}
        <div><span className="muted">{skills.form}</span><b>{player.form}</b></div>
        <div><span className="muted">{skills.experience}</span><b>{player.experience}</b></div>
      </div>
      <p className="sub" style={{ marginTop: 10 }}>
        {player.personality.aggressiveness} · {player.personality.agreeability} · {player.personality.honesty}
      </p>
    </div>
  );
}
