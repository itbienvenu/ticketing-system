// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path' // 👈 1. Import the 'path' module

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  
  resolve: {
    alias: {
      // Set the '@' alias to point to the absolute path of the 'src' directory
      '@': path.resolve(__dirname, './src'), 
    },
  },
})