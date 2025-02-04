/** @type {import('tailwindcss').Config} */
odule.exports = {
  content: [
    './templates/**/*.html',  // Chemin vers vos templates Django
    './static/js/**/*.js',    // Chemin vers vos fichiers JS (si nécessaire)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
