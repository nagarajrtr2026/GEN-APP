/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#050816',
          800: '#0b1020',
          700: '#111827',
        },
        accent: {
          cyan: '#06b6d4',
          violet: '#8b5cf6',
          purple: '#a855f7',
        }
      },
      animation: {
        'glow-pulse': 'glow 3s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 10px #8b5cf6, 0 0 20px #8b5cf6' },
          '100%': { boxShadow: '0 0 20px #06b6d4, 0 0 40px #06b6d4' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        }
      }
    },
  },
  plugins: [],
}