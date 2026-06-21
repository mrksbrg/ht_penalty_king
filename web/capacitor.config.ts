import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'io.github.mrksbrg.penaltyking',
  appName: 'Penalty King',
  webDir: 'dist',
  server: {
    // WASM (Pyodide) requires a secure context; 'https' scheme enables CDN fetches
    // without mixed-content blocks inside the Android WebView.
    androidScheme: 'https',
  },
};

export default config;
