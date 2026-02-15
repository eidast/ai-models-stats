import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["system-ui", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        mono: ["ui-monospace", "monospace"],
      },
      colors: {
        starquantix: {
          navy: "#0f172a",
          "navy-light": "#1e293b",
          "navy-lighter": "#334155",
          blue: "#2563eb",
          "blue-light": "#3b82f6",
          "blue-dark": "#1d4ed8",
        },
      },
    },
  },
  plugins: [],
};
export default config;
