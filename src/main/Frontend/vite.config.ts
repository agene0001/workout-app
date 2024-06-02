import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server:{
    proxy:{
      '/api/v1/recipes':{target:"http://localhost:8080"},
      '/recommendations': {target:"http://127.0.0.1:5000",
        changeOrigin: true},

    }
  }
})
