import { sveltekit } from '@sveltejs/kit/vite';
import { svelteTesting } from '@testing-library/svelte/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig, loadEnv } from 'vite';

// Define ports that don't change
const SPRING_PORT = 8081;
const hostIP = "0.0.0.0";
const port = 8080;
const protocol = "http";

// Use the function form of defineConfig
export default defineConfig(({ command, mode }) => {
  // Load .env files based on the mode
  loadEnv(mode, process.cwd(), ''); // Load all env vars without VITE_ prefix

  // Determine if we're in production based on Vite's mode
  const isProduction = mode === 'production';

  const SPRING_SERVICE = isProduction ? 'spring-backend' : 'localhost';
  const FLASK_SERVICE = isProduction ? 'flask-backend' : 'localhost';
  // Use development port 5000 for Flask unless in production mode
  const FLASK_PORT = isProduction ? 8082 : 5000;

  console.log(`[vite.config.ts] Running command: ${command}, mode: ${mode}`);

  // Create client environment variables if needed
  const clientEnv = {};

  return {
    plugins: [tailwindcss(), sveltekit()],
    
    // Define variables to be exposed to client-side code
    define: clientEnv,

    // Development server configuration
    server: {
      host: hostIP,
      port: port,
      proxy: {
        '/api/v1/recipes': {
          target: `${protocol}://${SPRING_SERVICE}:${SPRING_PORT}`,
          headers: { 'Cache-Control': 'no-store' },
          changeOrigin: true,
          secure: false,
        },
        "/recipes": {
          target: `${protocol}://${FLASK_SERVICE}:${FLASK_PORT}`,
          headers: { 'Cache-Control': 'no-store' },
          changeOrigin: true,
          secure: false,
        },
      }
    },

    // Production preview configuration
    preview: {
      allowedHosts: ['gainztrackers.com'],
      host: hostIP,
      port: port,
      proxy: {
        '/api/v1/recipes': {
          target: `${protocol}://${SPRING_SERVICE}:${SPRING_PORT}`,
          headers: { 'Cache-Control': 'no-store' },
          changeOrigin: true,
          secure: false,
        },
        "/recipes": {
          target: `${protocol}://${FLASK_SERVICE}:${FLASK_PORT}`,
          headers: { 'Cache-Control': 'no-store' },
          changeOrigin: true,
          secure: false,
        },
      }
    },
    
    // Keep the existing testing configuration
    test: {
      workspace: [
        {
          extends: './vite.config.ts',
          plugins: [svelteTesting()],
          test: {
            name: 'client',
            environment: 'jsdom',
            clearMocks: true,
            include: ['src/**/*.svelte.{test,spec}.{js,ts}'],
            exclude: ['src/lib/server/**'],
            setupFiles: ['./vitest-setup-client.ts']
          }
        },
        {
          extends: './vite.config.ts',
          test: {
            name: 'server',
            environment: 'node',
            include: ['src/**/*.{test,spec}.{js,ts}'],
            exclude: ['src/**/*.svelte.{test,spec}.{js,ts}']
          }
        }
      ]
    }
  };
});