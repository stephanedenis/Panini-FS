/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'panini-blue': '#0ea5e9',
        'panini-purple': '#8b5cf6',
        'panini-dark': '#1e293b',
      },
    },
  },
  plugins: [],
}
