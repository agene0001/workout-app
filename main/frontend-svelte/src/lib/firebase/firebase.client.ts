// src/lib/firebase/firebase.client.ts

import { initializeApp, getApps, getApp, type FirebaseApp } from "firebase/app";
import { getAuth, type Auth, connectAuthEmulator, onAuthStateChanged, type User } from "firebase/auth";
import { getFirestore, type Firestore, connectFirestoreEmulator } from "firebase/firestore";
import { getFunctions, type Functions, connectFunctionsEmulator } from "firebase/functions";
import { writable, type Writable } from "svelte/store";

// Firebase configuration object, populated from environment variables.
const firebaseConfigClient = {
    apiKey: import.meta.env.VITE_FIREBASE_API_KEY!,
    authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN!,
    projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID!,
    storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET!,
    messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID!,
    appId: import.meta.env.VITE_FIREBASE_APP_ID!,
    measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID!
};

// Singleton instances for Firebase app and services.
let clientApp: FirebaseApp | null = null;
let clientAuth: Auth | null = null;
let firestoreDb: Firestore | null = null;
let clientFunctions: Functions | null = null;

// Initialization promise
let initializationPromise: Promise<boolean> | null = null;

// Svelte stores for reactive state
export const currentUser: Writable<User | null> = writable(null);
export const isAdmin: Writable<boolean> = writable(false);
export const isInitialized: Writable<boolean> = writable(false);

// Default emulator host and ports.
const EMULATOR_HOST = "localhost";
const AUTH_EMULATOR_PORT = 9099;
const FIRESTORE_EMULATOR_PORT = 8083;
const FUNCTIONS_EMULATOR_PORT = 5001;

/**
 * Updates the admin status in the isAdmin store
 */
async function updateAdminStatus(user: User | null): Promise<void> {
    if (!user) {
        isAdmin.set(false);
        return;
    }

    try {
        const idTokenResult = await user.getIdTokenResult(true);
        const adminStatus = idTokenResult?.claims.admin === true;
        isAdmin.set(adminStatus);
    } catch (error) {
        console.error('Error checking admin status:', error);
        isAdmin.set(false);
    }
}

/**
 * Initializes the Firebase client application and services.
 * Returns a promise that resolves when initialization is complete.
 */
export function initializeFirebaseClient(): Promise<boolean> {
    // Return existing promise if initialization is in progress
    if (initializationPromise) {
        return initializationPromise;
    }

    // Skip if running on server
    if (typeof window === 'undefined') {
        return Promise.resolve(false);
    }

    console.log("Attempting Firebase client initialization...");

    initializationPromise = new Promise<boolean>((resolve) => {
        try {
            const appName = 'workout-app';
            const existingApp = getApps().find(app => app.name === appName);

            if (existingApp) {
                clientApp = existingApp;
            } else {
                clientApp = initializeApp(firebaseConfigClient, appName);
            }

            if (clientApp) {
                clientAuth = getAuth(clientApp);
                firestoreDb = getFirestore(clientApp);
                clientFunctions = getFunctions(clientApp);

                if (import.meta.env.DEV) {
                    console.log("Development mode detected. Connecting to Firebase emulators...");

                    if (clientAuth) {
                        connectAuthEmulator(clientAuth, `http://${EMULATOR_HOST}:${AUTH_EMULATOR_PORT}`, { disableWarnings: false });
                        console.log(`Auth connected to emulator at http://${EMULATOR_HOST}:${AUTH_EMULATOR_PORT}`);
                    }

                    if (firestoreDb) {
                        connectFirestoreEmulator(firestoreDb, EMULATOR_HOST, FIRESTORE_EMULATOR_PORT);
                        console.log(`Firestore connected to emulator at ${EMULATOR_HOST}:${FIRESTORE_EMULATOR_PORT}`);
                    }

                    if (clientFunctions) {
                        connectFunctionsEmulator(clientFunctions, EMULATOR_HOST, FUNCTIONS_EMULATOR_PORT);
                        console.log(`Functions connected to emulator at ${EMULATOR_HOST}:${FUNCTIONS_EMULATOR_PORT}`);
                    }
                } else {
                    console.log("Production mode detected. Connecting to live Firebase services.");
                }

                // Set up auth state listener
                if (clientAuth) {
                    onAuthStateChanged(clientAuth, (user) => {
                        currentUser.set(user);
                        updateAdminStatus(user);
                    });
                }

                isInitialized.set(true);
                console.log("Firebase client initialization process completed successfully.");
                resolve(true);
            } else {
                console.error("Failed to obtain Firebase app instance during initialization.");
                isInitialized.set(false);
                resolve(false);
            }
        } catch (error) {
            console.error("Firebase client initialization error:", error);
            clientApp = null;
            clientAuth = null;
            firestoreDb = null;
            clientFunctions = null;
            isInitialized.set(false);
            resolve(false);
        }
    });

    return initializationPromise;
}

/**
 * Returns a promise that resolves with the current user.
 * If no user is logged in, resolves with null.
 */
export function getCurrentUser(): Promise<User | null> {
    // First ensure Firebase is initialized
    return initializeFirebaseClient().then(() => {
        if (!clientAuth) {
            return null;
        }

        return clientAuth.currentUser;
    });
}

/**
 * Checks if the current user has admin privileges.
 * Returns a promise that resolves with true if user is an admin, false otherwise.
 */
export async function checkIsUserAdmin(): Promise<boolean> {
    try {
        // First ensure Firebase is initialized
        await initializeFirebaseClient();

        if (!clientAuth || !clientAuth.currentUser) {
            return false;
        }

        const user = clientAuth.currentUser;
        const idTokenResult = await user.getIdTokenResult(true);
        return idTokenResult?.claims.admin === true;
    } catch (error) {
        console.error('Error checking admin status:', error);
        return false;
    }
}

/**
 * Forces a refresh of the admin status.
 * Useful to call after admin status might have changed.
 */
export async function refreshAdminStatus(): Promise<boolean> {
    try {
        await initializeFirebaseClient();

        if (!clientAuth || !clientAuth.currentUser) {
            isAdmin.set(false);
            return false;
        }

        await updateAdminStatus(clientAuth.currentUser);

        // Return the current value
        let currentIsAdmin = false;
        isAdmin.subscribe(value => {
            currentIsAdmin = value;
        })();

        return currentIsAdmin;
    } catch (error) {
        console.error('Error refreshing admin status:', error);
        return false;
    }
}

/**
 * Returns the initialized Firebase App instance.
 */
export function getClientApp(): FirebaseApp | null {
    return clientApp;
}

/**
 * Returns the initialized Firebase Auth instance.
 */
export function getClientAuth(): Auth | null {
    return clientAuth;
}

/**
 * Returns the initialized Firebase Firestore instance.
 */
export function getDb(): Firestore | null {
    return firestoreDb;
}

/**
 * Returns the initialized Firebase Functions instance.
 */
export function getClientFunctions(): Functions | null {
    return clientFunctions;
}

/**
 * Checks if the Firebase client has been successfully initialized.
 */
export function isFirebaseClientInitialized(): boolean {
    return clientApp !== null && clientAuth !== null;
}

// Auto-initialize in browser environment
if (typeof window !== 'undefined') {
    initializeFirebaseClient();
}

// Export instances directly for convenience
export const app: FirebaseApp | null = clientApp;
export const auth: Auth | null = clientAuth;
export const db: Firestore | null = firestoreDb;
export const functions: Functions | null = clientFunctions;