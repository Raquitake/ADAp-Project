/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cudeca-green': '#2E7D32',
        'cudeca-green-dark': '#1B5E20',
        'cudeca-yellow': '#FFC107',
        'cudeca-orange': '#FF9800',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
