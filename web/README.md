# Penalty King — Web

Mobile-first web frontend. It runs the **same Python engine as the CLI** in the
browser via [Pyodide](https://pyodide.org) (WebAssembly), so the same HRF + seed
produces identical outcomes in the terminal and the browser. React is only a
viewer/controller — no game logic lives in TypeScript.

## Run

```bash
cd web
npm install
npm run dev      # copies the Python engine into public/engine, then starts Vite
```

Open the printed URL on a phone (same network) or in a desktop browser. First load
fetches Pyodide from the CDN (a few seconds).

## How it fits together

```
ht_penalty_king/*.py        ← the engine (source of truth, shared with the CLI)
   │  scripts/copy-engine.mjs copies it into ↓
web/public/engine/...        ← static copy bundled for the browser
   │  src/engine/pyodideEngine.ts loads it into Pyodide and calls engine.py
src/screens/*                ← React UI (Import → FastForward → Watch → Winner)
```

The UI only ever calls the functions in `ht_penalty_king/engine.py`
(`load_hrf`, `create_game`, `simulate_until_watch_threshold`, `get_current_shot`,
`advance_game`, `get_survivors`, `final_ranking`, `player_stats`).

## Build / Android

```bash
npm run build    # -> dist/
```

`base: "./"` keeps asset paths relative, so `dist/` can later be wrapped with
[Capacitor](https://capacitorjs.com) for an Android release without changes to the
game engine.

> Note: Pyodide is ~6–10 MB. That is the cost of running the real Python engine
> client-side with zero logic duplication and guaranteed seed-parity with the CLI.
> If startup size becomes a problem on phones, the alternative is a hand-ported
> TypeScript engine — but that duplicates logic and risks seed divergence.
