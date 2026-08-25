/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        blush: {
          50: "#FFF8F6",
          100: "#FDEAF0",
          200: "#F9D4E2",
        },
        lavender: {
          100: "#EFE3FB",
          200: "#D9C4F2",
          400: "#9B7EDE",
          500: "#8465C9",
        },
        peach: {
          100: "#FFE9DA",
          300: "#F6C89B",
          400: "#F2A65A",
        },
        rose: {
          400: "#EF87A8",
          500: "#E8749A",
          600: "#D65E85",
        },
        ink: {
          DEFAULT: "#3A2E3D",
          soft: "#6E5E71",
          muted: "#9C8B9F",
        },
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        body: ["'Plus Jakarta Sans'", "sans-serif"],
      },
      borderRadius: {
        blob: "42% 58% 65% 35% / 45% 40% 60% 55%",
      },
      keyframes: {
        drift: {
          "0%, 100%": { transform: "translate(0, 0) scale(1)" },
          "33%": { transform: "translate(18px, -24px) scale(1.05)" },
          "66%": { transform: "translate(-16px, 14px) scale(0.97)" },
        },
        driftSlow: {
          "0%, 100%": { transform: "translate(0, 0) scale(1)" },
          "50%": { transform: "translate(-22px, 20px) scale(1.06)" },
        },
        rise: {
          "0%": { opacity: "0", transform: "translateY(14px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        popIn: {
          "0%": { opacity: "0", transform: "scale(0.9)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        fillBar: {
          "0%": { width: "0%" },
        },
        pulseSoft: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.55" },
        },
      },
      animation: {
        drift: "drift 14s ease-in-out infinite",
        "drift-slow": "driftSlow 20s ease-in-out infinite",
        rise: "rise 0.5s ease-out both",
        "pop-in": "popIn 0.35s cubic-bezier(0.34,1.56,0.64,1) both",
        "pulse-soft": "pulseSoft 1.6s ease-in-out infinite",
      },
      boxShadow: {
        soft: "0 20px 60px -20px rgba(122, 76, 130, 0.35)",
        card: "0 10px 40px -12px rgba(122, 76, 130, 0.25)",
      },
    },
  },
  plugins: [],
};
