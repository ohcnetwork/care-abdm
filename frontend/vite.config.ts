import { defineConfig } from "vite";
import federation from "@originjs/vite-plugin-federation";
import path from "path";
import react from "@vitejs/plugin-react-swc";
import tailwindcss from "@tailwindcss/vite";
import { scopeTailwindOutput } from "./scripts/postcss-scope-plugin";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    federation({
      name: "care_abdm_fe",
      filename: "remoteEntry.js",
      exposes: {
        "./manifest": "./src/manifest.tsx",
      },
      shared: [
        "react",
        "react-dom",
        "react-i18next",
        "@tanstack/react-query",
        "raviger",
        "sonner",
      ],
    }),
    tailwindcss(),
    scopeTailwindOutput(),
    react(),
  ],
  build: {
    target: "esnext",
    minify: true,
    cssCodeSplit: false,
    // A federated remote must not emit <link rel=modulepreload>: the hints resolve against the
    // host origin and 404 there (observed as ~25 console errors per page on 2026-09-15).
    modulePreload: false,
    rollupOptions: {
      external: [],
      input: {
        main: "./src/index.tsx",
      },
      output: {
        format: "esm",
      },
    },
  },
  experimental: {
    // The federation runtime appends the stylesheet as a <link> from the remote origin. A URL
    // inside that CSS (the Geist Mono woff2) must be relative to the CSS file, or the browser
    // resolves `/assets/...` against the host origin and 404s (the modulepreload case above).
    // JS references keep Vite's default.
    renderBuiltUrl(_filename, { hostType }) {
      return hostType === "css" ? { relative: true } : undefined;
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      // @base-ui/react's stores import the CommonJS-only
      // `use-sync-external-store` shim. Under @originjs/vite-plugin-federation,
      // a CJS `require("react")` is NOT rewritten to the shared (host) React,
      // so it binds to the remote's *bundled* React whose dispatcher is null:
      //   "Cannot read properties of null (reading 'useSyncExternalStore')"
      // Aliasing to ESM files that import React as a bare specifier lets
      // federation route them to the single shared instance.
      // Same fix as care_excalidraw_fe/vite.config.ts.
      "use-sync-external-store/shim/with-selector.js": path.resolve(
        __dirname,
        "./src/shims/with-selector.ts",
      ),
      "use-sync-external-store/shim/with-selector": path.resolve(
        __dirname,
        "./src/shims/with-selector.ts",
      ),
      "use-sync-external-store/shim/index.js": path.resolve(
        __dirname,
        "./src/shims/shim.ts",
      ),
      "use-sync-external-store/shim": path.resolve(
        __dirname,
        "./src/shims/shim.ts",
      ),
    },
  },
  server: {
    port: Number(process.env.PORT) || 4173,
    strictPort: !!process.env.PORT,
    allowedHosts: true,
    host: "0.0.0.0",
  },
  preview: {
    port: Number(process.env.PORT) || 4173,
    allowedHosts: true,
    host: "0.0.0.0",
    cors: true,
  },
});
