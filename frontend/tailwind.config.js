/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gov: {
          50: '#f0f4f8',
          100: '#d9e2ec',
          500: '#102a43',
          600: '#0b1b2b',
          700: '#091522',
        },
        accent: {
          blue: '#2563eb',
          amber: '#f59e0b',
          green: '#10b981',
          red: '#ef4444',
        }
      }
    },
  },
  plugins: [],
}
