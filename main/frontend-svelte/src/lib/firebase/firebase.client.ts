// src/lib/firebase/firebase.client.ts

import { initializeApp, getApps, getApp, type FirebaseApp } from "firebase/app";
import { getAuth, type Auth, connectAuthEmulator } from "firebase/auth";
import { getFirestore, type Firestore, connectFirestoreEmulator } from "firebase/firestore";
import { getFunctions, type Functions, connectFunctionsEmulator } from "firebase/functions"; // Added Functions

// Firebase configuration object, populated from environment variables.
// VITE_ prefix is standard for Vite projects to expose env vars to the client.
const firebaseConfigClient = {
    apiKey: import.meta.env.VITE_FIREBASE_API_KEY!,
    authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN!,
    projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID!,
    storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET!,
    messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID!,
    appId: import.meta.env.VITE_FIREBASE_APP_ID!,
    measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID!
};
export async function checkIsUserAdmin() {
    if (!isFirebaseClientInitialized()) {
        console.warn('Admin check: Firebase client not initialized.');
        return false;
    }
    const authInstance = getClientAuth(); // Or firebaseAuth;
    if (!authInstance || !authInstance.currentUser) {
        console.warn('Admin check: No user is currently logged in.');
        return false;
    }
    try {
        const idTokenResult = await authInstance.currentUser.getIdTokenResult(true);
        return idTokenResult?.claims.admin === true;
    } catch (error) {
        console.error('Error checking admin status:', error);
        alert('Could not verify admin privileges. Please try again.');
        return false;
    }
}
// Singleton instances for Firebase app and services.
let clientApp: FirebaseApp | null = null;
let clientAuth: Auth | null = null;
let firestoreDb: Firestore | null = null;
let clientFunctions: Functions | null = null; // Added Functions instance
let isInitialized = false; // Flag to track initialization status.

// Default emulator host and ports.
// Ensure these match your firebase.json emulator configuration.
const EMULATOR_HOST = "localhost"; // Or "127.0.0.1"
const AUTH_EMULATOR_PORT = 9099;
const FIRESTORE_EMULATOR_PORT = 8083;
const FUNCTIONS_EMULATOR_PORT = 5001; // Added Functions emulator port

/**
 * Initializes the Firebase client application and services.
 * If in a development environment (import.meta.env.DEV is true),
 * it will attempt to connect to the Firebase emulators.
 */
export function initializeFirebaseClient(): void {
    // Prevent re-initialization or running on the server.
    if (isInitialized || typeof window === 'undefined') {
        if (isInitialized) {
            // console.log("Firebase client already initialized.");
        }
        return;
    }

    console.log("Attempting Firebase client initialization...");

    try {
        const appName = 'workout-app'; // Consistent app name
        const existingApp = getApps().find(app => app.name === appName);

        if (existingApp) {
            clientApp = existingApp;
        } else {
            clientApp = initializeApp(firebaseConfigClient, appName);
        }

        if (clientApp) {
            clientAuth = getAuth(clientApp);
            firestoreDb = getFirestore(clientApp);
            clientFunctions = getFunctions(clientApp); // Initialize Functions

            if (import.meta.env.DEV) {
                console.log("Development mode detected. Attempting to connect to Firebase emulators...");

                if (clientAuth) {
                    connectAuthEmulator(clientAuth, `http://${EMULATOR_HOST}:${AUTH_EMULATOR_PORT}`, { disableWarnings: false });
                    console.log(`Auth connected to emulator at http://${EMULATOR_HOST}:${AUTH_EMULATOR_PORT}`);
                } else {
                    console.warn("Auth instance not available for emulator connection.");
                }

                if (firestoreDb) {
                    connectFirestoreEmulator(firestoreDb, EMULATOR_HOST, FIRESTORE_EMULATOR_PORT);
                    console.log(`Firestore connected to emulator at ${EMULATOR_HOST}:${FIRESTORE_EMULATOR_PORT}`);
                } else {
                    console.warn("Firestore instance not available for emulator connection.");
                }

                if (clientFunctions) { // Connect Functions emulator
                    connectFunctionsEmulator(clientFunctions, EMULATOR_HOST, FUNCTIONS_EMULATOR_PORT);
                    console.log(`Functions connected to emulator at ${EMULATOR_HOST}:${FUNCTIONS_EMULATOR_PORT}`);
                } else {
                    console.warn("Functions instance not available for emulator connection.");
                }
            } else {
                console.log("Production mode detected. Connecting to live Firebase services.");
            }

            isInitialized = true;
            console.log("Firebase client initialization process completed successfully.");
        } else {
            console.error("Failed to obtain Firebase app instance during initialization.");
            isInitialized = false;
        }

    } catch (error) {
        console.error("Firebase client initialization error:", error);
        clientApp = null;
        clientAuth = null;
        firestoreDb = null;
        clientFunctions = null; // Reset functions instance on error
        isInitialized = false;
    }
}

/**
 * Returns the initialized Firebase App instance.
 * @returns {FirebaseApp | null} The FirebaseApp instance or null if not initialized.
 */
export function getClientApp(): FirebaseApp | null { return clientApp; }

/**
 * Returns the initialized Firebase Auth instance.
 * @returns {Auth | null} The Auth instance or null if not initialized.
 */
export function getClientAuth(): Auth | null { return clientAuth; }

/**
 * Returns the initialized Firebase Firestore instance.
 * @returns {Firestore | null} The Firestore instance or null if not initialized.
 */
export function getDb(): Firestore | null { return firestoreDb; }

/**
 * Returns the initialized Firebase Functions instance.
 * @returns {Functions | null} The Functions instance or null if not initialized.
 */
export function getClientFunctions(): Functions | null { return clientFunctions; }


/**
 * Checks if the Firebase client has been successfully initialized.
 * @returns {boolean} True if initialized, false otherwise.
 */
export function isFirebaseClientInitialized(): boolean { return isInitialized; }

// Auto-initialize in browser environment
if (typeof window !== 'undefined') {
    initializeFirebaseClient();
}

// Export instances directly for convenience, ensuring they are only accessed after initialization.
// Consumers should ideally check isFirebaseClientInitialized() or use a store that depends on it.
// However, for direct imports like in authStore.js, these can be helpful.
// Note: These will be null until initializeFirebaseClient completes.
export const app: FirebaseApp | null = getClientApp();
export const auth: Auth | null = getClientAuth();
export const db: Firestore | null = getDb();
export const functions: Functions | null = getClientFunctions();
