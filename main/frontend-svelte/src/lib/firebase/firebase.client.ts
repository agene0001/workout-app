// src/lib/firebase/firebase.client.ts

import { initializeApp, getApps, getApp, type FirebaseApp } from "firebase/app";
import { getAuth, type Auth } from "firebase/auth";
// Import PUBLIC variables - these MUST start with VITE_ and be set at BUILD time
const env = import.meta.env.VITE_FIREBASE_API_KEY!=null ? import.meta.env : process.env;

const firebaseConfigClient = {
    apiKey: env.VITE_FIREBASE_API_KEY,
    authDomain: env.VITE_FIREBASE_AUTH_DOMAIN,
    projectId: env.VITE_FIREBASE_PROJECT_ID,
    storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: env.VITE_FIREBASE_MESSAGING_SENDER_ID,
    appId: env.VITE_FIREBASE_APP_ID,
    measurementId: env.VITE_FIREBASE_MEASUREMENT_ID
};

// Initialize Client-Side App (ensure singleton pattern)
let clientApp: FirebaseApp;
let clientAuth: Auth;
try {
       clientApp = getApps().find(app => app.name === 'client') || initializeApp(firebaseConfigClient, 'client');
       clientAuth = getAuth(clientApp);
} catch (error) {
    console.error("Firebase initialization error:", error);
    // Provide a fallback or graceful degradation
}
export { clientApp, clientAuth };
// Initialize other client-side services like Firestore client, Analytics here