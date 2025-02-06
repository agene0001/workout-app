import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Define ports and services based on environment
const SPRING_PORT = 8081;
const SPRING_SERVICE = process.env.NODE_ENV === 'production' ? 'spring-backend' : 'localhost';

export default defineConfig({
  plugins: [react()],

  // Development server configuration
  server: {
    host: "0.0.0.0",
    port: 8080,
    proxy: {
      '/api/v1/recipes': {
        target: `http://${SPRING_SERVICE}:${SPRING_PORT}`,
        headers: {
          'Cache-Control': 'no-store',
        },
        changeOrigin: true,
        secure: false

      }

    }
  },

  // Production preview configuration - this is what's used in Kubernetes
  preview: {
    host: "0.0.0.0",
    port: 8080,
    proxy: {
      '/api/v1/recipes': {
        target: `http://${SPRING_SERVICE}:${SPRING_PORT}`,
        headers: {
          'Cache-Control': 'no-store',
        },
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      },

    }
  }
})