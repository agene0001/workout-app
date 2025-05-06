// src/lib/firebase/firebase.client.ts

import { initializeApp, getApps, getApp, type FirebaseApp } from "firebase/app";
import { getAuth, type Auth } from "firebase/auth";
import { getFirestore, type Firestore } from "firebase/firestore"; // Import Firestore type

const firebaseConfigClient = {
    apiKey: import.meta.env.VITE_FIREBASE_API_KEY!,
    authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN!,
    projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID!,
    storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET!,
    messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID!,
    appId: import.meta.env.VITE_FIREBASE_APP_ID!,
    measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID!
};

let clientApp: FirebaseApp | null = null;
let clientAuth: Auth | null = null;
let firestoreDb: Firestore | null = null; // Add Firestore instance
let isInitialized = false;

// *** THE INITIALIZATION FUNCTION ***
export function initializeFirebaseClient(): void {
    if (isInitialized || typeof window === 'undefined') { // Add check for browser environment
        return; // Prevent double init or server-side run
    }

    console.log("Attempting Firebase client initialization...");

    try {
        const appName = 'client-default'; // Use a consistent name
        const existingApp = getApps().find(app => app.name === appName);

        if (existingApp) {
            clientApp = existingApp;
        } else {
            clientApp = initializeApp(firebaseConfigClient, appName);
        }

        if (clientApp) {
            clientAuth = getAuth(clientApp);
            firestoreDb = getFirestore(clientApp); // Initialize Firestore here too
            isInitialized = true;
            console.log("Firebase client initialized successfully.");
        } else {
            console.error("Failed to obtain Firebase app instance.");
            isInitialized = false;
        }

    } catch (error) {
        console.error("Firebase client initialization error:", error);
        clientApp = null;
        clientAuth = null;
        firestoreDb = null;
        isInitialized = false;
    }
}

// Getters - return null if not initialized
export function getClientApp(): FirebaseApp | null { return clientApp; }
export function getClientAuth(): Auth | null { return clientAuth; }
export function getDb(): Firestore | null { return firestoreDb; } // Export Firestore getter
export function isFirebaseClientInitialized(): boolean { return isInitialized; }