/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f4ff',
          100: '#d9e2ff',
          200: '#bad0ff',
          300: '#8fb1ff',
          400: '#5c8aff',
          500: '#335eff',
          600: '#1a3eff',
          700: '#0026e6',
          800: '#001fb3',
          900: '#001a80',
          DEFAULT: '#335eff',
        },
        sage: {
          50: '#f2f9f6',
          100: '#e1f1e9',
          500: '#10b981',
          DEFAULT: '#10b981',
        },
        heritage: {
          krem: '#FAF9F6',
          gold: '#D4AF37',
          deep: '#1A1A1A',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.1) 100%)',
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.07)',
        'premium': '0 20px 50px -12px rgba(0, 0, 0, 0.05)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      }
    },
  },
  plugins: [],
}
