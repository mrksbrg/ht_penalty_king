// Copies the authoritative Python engine into public/engine so Pyodide can load
// it in the browser. This is the SAME source as the CLI — no logic is duplicated;
// the files are just bundled as static assets. Re-run via `npm run copy-engine`
// (also runs automatically before dev/build).

import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const pkgRoot = path.resolve(here, "..", ".."); // ht_penalty_king/
const outRoot = path.resolve(here, "..", "public", "engine", "ht_penalty_king");

// Modules the engine needs (game logic stays Python, outside React).
const MODULES = [
  "__init__.py", "config.py", "hrf_parser.py", "profiles.py", "penalty.py",
  "game.py", "report.py", "narrator.py", "i18n.py", "montecarlo.py", "engine.py",
];
const LANG_DIR = "languages";

async function main() {
  await fs.rm(outRoot, { recursive: true, force: true });
  await fs.mkdir(outRoot, { recursive: true });
  const manifest = [];

  for (const m of MODULES) {
    await fs.copyFile(path.join(pkgRoot, m), path.join(outRoot, m));
    manifest.push(`ht_penalty_king/${m}`);
  }

  const langOut = path.join(outRoot, LANG_DIR);
  await fs.mkdir(langOut, { recursive: true });
  for (const f of await fs.readdir(path.join(pkgRoot, LANG_DIR))) {
    if (!f.endsWith(".py")) continue;
    await fs.copyFile(path.join(pkgRoot, LANG_DIR, f), path.join(langOut, f));
    manifest.push(`ht_penalty_king/${LANG_DIR}/${f}`);
  }

  await fs.writeFile(
    path.resolve(here, "..", "public", "engine", "manifest.json"),
    JSON.stringify(manifest, null, 2),
  );
  console.log(`copied ${manifest.length} engine files -> public/engine/`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
