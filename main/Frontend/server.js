import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import request from 'request';

// Constants for proxy ports
const SPRING_PORT = 8081;
const PYTHON_PORT = 8082;
const FRONTEND_PORT = 8080;

const app = express();

// Resolve the current directory (ESM-specific)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Serve static files from the 'dist' folder
app.use(express.static(path.join(__dirname, 'dist')));

// Proxy `/api/v1/recipes` to Spring Boot backend
app.use('/api/v1/recipes', (req, res) => {
    const proxyUrl = `http://spring-backend:${SPRING_PORT}${req.originalUrl}`;
    req.pipe(request(proxyUrl)).pipe(res);
});

// Proxy `/recommendations` and `/build_recipes` to Python backend
app.use(['/recommendations', '/build_recipes'], (req, res) => {
    const proxyUrl = `http://localhost:${PYTHON_PORT}${req.originalUrl}`;
    req.pipe(request(proxyUrl)).pipe(res);
});

// Serve the frontend index.html for all other routes
app.get('*', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'dist', 'index.html'));
});

// Start the server on port 8080
app.listen(FRONTEND_PORT, '0.0.0.0', () => {
    console.log(`Frontend running at http://localhost:${FRONTEND_PORT}`);
});
