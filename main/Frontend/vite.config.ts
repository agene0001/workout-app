import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
const PYTHON_PORT = 8082;
const SPRING_PORT = 8081;
// const FRONTEND_PORT =
const SPRING_SERVICE = process.env.NODE_ENV === 'production' ? 'spring-backend' : 'localhost';
const PYTHON_SERVICE = process.env.NODE_ENV === 'production' ? 'python-api' : 'localhost';
    // || 'http://localhost';
// console.log('====== VITE CONFIG ======');
// console.log('NODE_ENV:', process.env.NODE_ENV);
// console.log('SPRING_SERVICE:', SPRING_SERVICE);
// // console.log('TARGET_URL:', TARGET_URL);
// console.log('========================');
export default defineConfig({

  plugins: [react()],
  server:{
    host:"0.0.0.0",
    port:8080,
    proxy:{
      '/api/v1/recipes': {
        target: `http://${SPRING_SERVICE}:${SPRING_PORT}`,
        headers: {
          'Cache-Control': 'no-store',
        },
        changeOrigin: true,

      },
      '/recommendations': {target:`http://${PYTHON_SERVICE}:${PYTHON_PORT}`,
        changeOrigin: true},
      '/build_recipes': {target:`http://${PYTHON_SERVICE}:${PYTHON_PORT}`,
        changeOrigin: true},


    }

  }
})
