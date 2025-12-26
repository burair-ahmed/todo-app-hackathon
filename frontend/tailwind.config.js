/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Horizon Design System - HSL based for better tinting
        horizon: {
          50: '#f0f9f8',
          100: '#d9f0ed',
          200: '#91C6BC', // Primary Mint
          300: '#4B9DA9', // Primary Ocean
          400: '#3a7a84',
          500: '#2d5e66',
          600: '#234a50',
          700: '#1a373b',
          800: '#122629',
          900: '#0a1618',
        },
        accent: {
          light: "#F6F3C2", // Cream
          DEFAULT: "#E37434", // Sunset
          dark: "#c25e25",
        },
        background: {
          surface: "#ffffff",
          soft: "#f8fafc",
          muted: "#f1f5f9",
        }
      },
      backgroundImage: {
        'horizon-mesh': "radial-gradient(at 0% 0%, hsla(169,32%,68%,0.15) 0px, transparent 50%), radial-gradient(at 100% 0%, hsla(188,38%,47%,0.1) 0px, transparent 50%), radial-gradient(at 100% 100%, hsla(21,75%,55%,0.08) 0px, transparent 50%), radial-gradient(at 0% 100%, hsla(169,32%,68%,0.1) 0px, transparent 50%)",
        'glass-gradient': "linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.1) 100%)",
        'premium-gradient': "linear-gradient(135deg, #91C6BC 0%, #4B9DA9 100%)",
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(75, 157, 169, 0.15)',
        'glass-hover': '0 12px 40px 0 rgba(75, 157, 169, 0.25)',
        'soft-float': '0 20px 50px -12px rgba(0, 0, 0, 0.08)',
        'inner-glass': 'inset 0 1px 1px 0 rgba(255, 255, 255, 0.3)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'fade-in': 'fade-in 0.5s ease-out forwards',
        'slide-up': 'slide-up 0.5s ease-out forwards',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'shimmer': {
          '100%': { transform: 'translateX(100%)' },
        }
      }
    },
  },
  plugins: [],
};
