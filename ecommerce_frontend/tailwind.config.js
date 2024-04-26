/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    container: {
      padding: '2rem',
    },
    extend: {
      colors: {
        primary: "#fd3d57",
      },
    },
  },
  plugins: [],
}