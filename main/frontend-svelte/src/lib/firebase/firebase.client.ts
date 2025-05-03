// src/lib/firebase/firebase.client.ts

import { initializeApp, getApps, getApp, type FirebaseApp } from "firebase/app";
import { getAuth, type Auth } from "firebase/auth";
// Import PUBLIC variables - these MUST start with VITE_ and be set at BUILD time
const env = import.meta.env;

const firebaseConfigClient = {
    apiKey: 'AIzaSyCBaEACR9uDD9ISJ092h2o6y5UzOdY_sJU',
    authDomain: 'workout-app-441723.firebaseapp.com',
    projectId: 'workout-app-441723',
    storageBucket: 'workout-app-441723.firebasestorage.app',
    messagingSenderId: '209783809936',
    appId: '1:209783809936:web:fd21752b8673cad1dcb515',
    measurementId: 'G-RWGLFL9CPN'
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