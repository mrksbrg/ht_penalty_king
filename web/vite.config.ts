import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Pyodide is loaded from the CDN at runtime; nothing special needed here.
// base "./" keeps asset paths relative so the build works inside Capacitor too.
export default defineConfig({
  base: "./",
  plugins: [react()],
  server: { host: true },
});
