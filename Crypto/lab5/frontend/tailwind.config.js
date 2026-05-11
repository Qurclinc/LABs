export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // base
        bg: "#1a1b26",
        surface: "#24283b",
        surface2: "#1f2335",
        border: "#414868",

        // text
        text: "#c0caf5",
        muted: "#565f89",

        // accents
        blue: "#7aa2f7",
        cyan: "#7dcfff",
        green: "#9ece6a",
        yellow: "#e0af68",
        orange: "#ff9e64",
        red: "#f7768e",
        magenta: "#bb9af7",
        purple: "#9d7cd8",

        // aliases
        primary: "#7aa2f7",
        success: "#9ece6a",
        danger: "#f7768e",
        warning: "#e0af68",
        accent: "#bb9af7",
      },

      boxShadow: {

        neonBlue: "0 0 10px #7aa2f7, 0 0 20px #7aa2f7",
        neonGreen: "0 0 10px #9ece6a, 0 0 20px #9ece6a",
        neonRed: "0 0 10px #f7768e, 0 0 20px #f7768e",
        neonPurple: "0 0 10px #bb9af7, 0 0 20px #bb9af7",
        neonMuted: "0 0 10px #565f89, 0 0 20px #565f89"
      },

      dropShadow: {
        neon: "0 0 6px rgba(122,162,247,0.8)"
      }
    }
  },
  plugins: []
}
