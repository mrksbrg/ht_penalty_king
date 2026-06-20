export function PrickMeter({ prickar }: { prickar: number }) {
  const n = Math.max(0, Math.min(5, prickar));
  return <span className="meter">{"●".repeat(n)}{"○".repeat(5 - n)}</span>;
}
