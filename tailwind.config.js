/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html"],
  theme: {
    extend: {
      colors:{
        "py-yellow":"#F2C335",
        "py-yellow-light":"#F2D57E",
        "py-yellow-dark":"#BF9004",
        "py-blue":"#377BA6",
        "py-blue-dark":"#295773",
      },
    },
   
  },
  plugins: [],
}

// **表示不管多少層