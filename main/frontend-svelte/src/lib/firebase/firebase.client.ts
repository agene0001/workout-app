// src/lib/firebase/firebase.client.ts
import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Import PUBLIC variables - these MUST start with VITE_ and be set at BUILD time
import { env } from '$env/dynamic/public';

const firebaseConfigClient = {
    apiKey: env.PUBLIC_FIREBASE_API_KEY,
    authDomain: env.PUBLIC_FIREBASE_AUTH_DOMAIN,
    projectId: env.PUBLIC_FIREBASE_PROJECT_ID,
    storageBucket: env.PUBLIC_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: env.PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
    appId: env.PUBLIC_FIREBASE_APP_ID,
    measurementId: env.PUBLIC_FIREBASE_MEASUREMENT_ID
};

// Initialize Client-Side App (ensure singleton pattern)
export const clientApp = getApps().find(app => app.name === 'client') || initializeApp(firebaseConfigClient, 'client');
export const clientAuth = getAuth(clientApp);

// Initialize other client-side services like Firestore client, Analytics here