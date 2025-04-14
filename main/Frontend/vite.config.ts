import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
// Define ports that don't change
const SPRING_PORT = 8081;
const hostIP = "0.0.0.0";
const port = 8080;
const protocol = "http";

// Use the function form of defineConfig
export default defineConfig(({ command, mode }) => {
  // Load .env files based on the mode
  // This loads .env, .env.local, .env.[mode], .env.[mode].local
  // Note: This primarily affects VITE_* variables, but can load others too.
  // process.env will still hold variables from the execution environment (like from docker-compose)
  loadEnv(mode, process.cwd(), ''); // Load all env vars without VITE_ prefix

  // Determine if we are in production based on Vite's mode
  // 'mode' is more reliable within Vite config than process.env.NODE_ENV directly
  const isProduction = mode === 'production';

  const SPRING_SERVICE = isProduction ? 'spring-backend' : 'localhost';
  const FLASK_SERVICE = isProduction ? 'flask-backend' : 'localhost';
  // Use development port 5000 for Flask unless in production mode
  const FLASK_PORT = isProduction ? 8082 : 5000;

  console.log(`[vite.config.ts] Running command: ${command}, mode: ${mode}`);
  // console.log(`[vite.config.ts] isProduction: ${isProduction}`);
  // console.log(`[vite.config.ts] SPRING_SERVICE: ${SPRING_SERVICE}`);
  // console.log(`[vite.config.ts] FLASK_SERVICE: ${FLASK_SERVICE}`);
  // console.log(`[vite.config.ts] FLASK_PORT: ${FLASK_PORT}`);
  // // You can also check the actual env var from docker-compose if needed for debugging:
  // console.log(`[vite.config.ts] process.env.NODE_ENV: ${process.env.NODE_ENV}`);


  // Use define carefully - expose only what's needed on the client
  // Avoid exposing all of process.env
  const clientEnv = {};
  // Example: If you need NODE_ENV on the client (generally not recommended)
  // clientEnv['process.env.NODE_ENV'] = JSON.stringify(mode);
  // Example: If you need a specific API endpoint on the client
  // clientEnv['import.meta.env.VITE_API_BASE_URL'] = JSON.stringify(isProduction ? 'https://api.yoursite.com' : '/api'); // Use VITE_ prefix by convention


  return {
    plugins: [react(), tailwindcss(),],

    // Define variables to be exposed to client-side code
    // Prefer using import.meta.env and VITE_ prefixes
    define: clientEnv, // Use the filtered object

    // Development server configuration
    server: {
      host: hostIP,
      port: port,
      proxy: {
        '/api/v1/recipes': {
          // Use dev values for 'vite dev' (mode='development')
          target: `${protocol}://localhost:${SPRING_PORT}`,
          headers: { 'Cache-Control': 'no-store' },
          changeOrigin: true,
          secure: false,
        },
        "/recipes": {
          // Use dev values for 'vite dev' (mode='development')
          target: `${protocol}://localhost:5000`, // Flask dev port
          headers: { 'Cache-Control': 'no-store' },
          changeOrigin: true,
          secure: false,
        }
      }
    },

    // Production preview configuration (used by 'vite preview')
    preview: {
      allowedHosts: ['gainztrackers.com'], // Add your actual domain if needed
      host: hostIP,
      port: port,
      proxy: {
        '/api/v1/recipes': {
          // Uses values determined by 'mode' when 'vite preview' runs
          target: `${protocol}://${SPRING_SERVICE}:${SPRING_PORT}`,
          headers: { 'Cache-Control': 'no-store' },
          changeOrigin: true,
          secure: false,
          // rewrite: (path) => path // Usually not needed unless changing the path structure
        },
        "/recipes": {
          // Uses values determined by 'mode' when 'vite preview' runs
          target: `${protocol}://${FLASK_SERVICE}:${FLASK_PORT}`,
          headers: { 'Cache-Control': 'no-store' },
          changeOrigin: true,
          secure: false,
        }
      }
    }
  };
});