/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#1a1b26",  
        surface: "#24283b",     
        surfaceDark: "#181926",

        // неоновые акценты
        primary: "#7aa2f7",   // синий
        secondary: "#9ece6a", // зеленый
        accent: "#f7768e",    // красный/розовый
        purple: "#bb9af7",    // фиолетовый
        cyan: "#7dcfff",      // голубой

        // текст
        text: "#c0caf5",
        muted: "#565f89",
        error: "#f7768e",
        highlight: "#9d7cd8",
      },
      boxShadow: {
        neonBlue: "0 0 10px #7aa2f7, 0 0 20px rgba(122,162,247,0.6)",
        neonPink: "0 0 10px #f7768e, 0 0 20px rgba(247,118,142,0.6)",
        neonPurple: "0 0 10px #bb9af7, 0 0 20px rgba(187,154,247,0.6)",
      },
    },
  },
  plugins: [],
}

