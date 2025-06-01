// src/lib/firebase/firebase.client.ts

import { initializeApp, getApps, getApp, type FirebaseApp } from "firebase/app";
import { getAuth, type Auth, connectAuthEmulator, onAuthStateChanged, type User } from "firebase/auth";
import { getFirestore, type Firestore, connectFirestoreEmulator } from "firebase/firestore";
import { getFunctions, type Functions, connectFunctionsEmulator } from "firebase/functions";
import { writable, type Writable, get } from "svelte/store"; // Ensure 'get' is imported

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

// --- MODIFIED: Use Svelte Stores for all instances ---
export const firebaseAppStore: Writable<FirebaseApp | null> = writable(null);
export const firebaseAuthStore: Writable<Auth | null> = writable(null);
export const firestoreDbStore: Writable<Firestore | null> = writable(null);
export const firebaseFunctionsStore: Writable<Functions | null> = writable(null);
// --- END MODIFIED ---

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
        const authInstance = get(firebaseAuthStore); // Read from the store
        if (!authInstance) {
            console.warn("Auth instance not available for admin status check.");
            isAdmin.set(false);
            return;
        }
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

    // Skip if running on server (SSR)
    if (typeof window === 'undefined') {
        return Promise.resolve(false);
    }

    // console.log("Attempting Firebase client initialization...");

    initializationPromise = new Promise<boolean>((resolve) => {
        try {
            const appName = 'workout-app';
            const existingApp = getApps().find(app => app.name === appName);

            let appInstance: FirebaseApp;
            if (existingApp) {
                appInstance = existingApp;
            } else {
                appInstance = initializeApp(firebaseConfigClient, appName);
            }
            firebaseAppStore.set(appInstance); // Update the store

            let authInstance = getAuth(appInstance);
            firebaseAuthStore.set(authInstance); // Update the store

            let dbInstance = getFirestore(appInstance,'docs');
            firestoreDbStore.set(dbInstance); // Update the store

            let functionsInstance = getFunctions(appInstance);
            firebaseFunctionsStore.set(functionsInstance); // Update the store


            if (import.meta.env.DEV) {
                console.log("Development mode detected. Connecting to Firebase emulators...");

                if (authInstance) {
                    connectAuthEmulator(authInstance, `http://${EMULATOR_HOST}:${AUTH_EMULATOR_PORT}`, { disableWarnings: false });
                    console.log(`Auth connected to emulator at http://${EMULATOR_HOST}:${AUTH_EMULATOR_PORT}`);
                }

                if (dbInstance) {
                    connectFirestoreEmulator(dbInstance, EMULATOR_HOST, FIRESTORE_EMULATOR_PORT);
                    console.log(`Firestore connected to emulator at ${EMULATOR_HOST}:${FIRESTORE_EMULATOR_PORT}`);
                }

                if (functionsInstance) {
                    connectFunctionsEmulator(functionsInstance, EMULATOR_HOST, FUNCTIONS_EMULATOR_PORT);
                    console.log(`Functions connected to emulator at ${EMULATOR_HOST}:${FUNCTIONS_EMULATOR_PORT}`);
                }
            } else {
                console.log("Production mode detected. Connecting to live Firebase services.");
            }

            // Set up auth state listener
            if (authInstance) {
                onAuthStateChanged(authInstance, (user) => {
                    currentUser.set(user);
                    updateAdminStatus(user);
                });
            }

            isInitialized.set(true);
            console.log("Firebase client initialization process completed successfully.");
            resolve(true);

        } catch (error) {
            console.error("Firebase client initialization error:", error);
            firebaseAppStore.set(null); // Reset stores on error
            firebaseAuthStore.set(null);
            firestoreDbStore.set(null);
            firebaseFunctionsStore.set(null);
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
    return initializeFirebaseClient().then(() => {
        const authInstance = get(firebaseAuthStore);
        if (!authInstance) {
            return null;
        }
        return authInstance.currentUser;
    });
}

/**
 * Checks if the current user has admin privileges.
 * Returns a promise that resolves with true if user is an admin, false otherwise.
 */
export async function checkIsUserAdmin(): Promise<boolean> {
    try {
        await initializeFirebaseClient();
        const authInstance = get(firebaseAuthStore);
        if (!authInstance || !authInstance.currentUser) {
            return false;
        }
        const user = authInstance.currentUser;
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
        const authInstance = get(firebaseAuthStore);
        if (!authInstance || !authInstance.currentUser) {
            isAdmin.set(false);
            return false;
        }
        await updateAdminStatus(authInstance.currentUser);
        let currentIsAdmin = false;
        isAdmin.subscribe(value => { currentIsAdmin = value; })();
        return currentIsAdmin;
    } catch (error) {
        console.error('Error refreshing admin status:', error);
        return false;
    }
}

/**
 * Returns the initialized Firebase App instance (reading from the store).
 * @deprecated Use firebaseAppStore.subscribe() or get(firebaseAppStore) for reactive access.
 */
export function getClientApp(): FirebaseApp | null {
    return get(firebaseAppStore);
}

/**
 * Returns the initialized Firebase Auth instance (reading from the store).
 * @deprecated Use firebaseAuthStore.subscribe() or get(firebaseAuthStore) for reactive access.
 */
export function getClientAuth(): Auth | null {
    return get(firebaseAuthStore);
}

/**
 * Returns the initialized Firebase Firestore instance (reading from the store).
 * @deprecated Use firestoreDbStore.subscribe() or get(firestoreDbStore) for reactive access.
 */
export function getDb(): Firestore | null {
    return get(firestoreDbStore);
}

/**
 * Returns the initialized Firebase Functions instance (reading from the store).
 * @deprecated Use firebaseFunctionsStore.subscribe() or get(firebaseFunctionsStore) for reactive access.
 */
export function getClientFunctions(): Functions | null {
    return get(firebaseFunctionsStore);
}

/**
 * Checks if the Firebase client has been successfully initialized.
 * @deprecated Use isInitialized store for reactivity.
 */
export function isFirebaseClientInitialized(): boolean {
    return get(isInitialized); // Read from the store
}


// Auto-initialize in browser environment
if (typeof window !== 'undefined') {
    initializeFirebaseClient();
}