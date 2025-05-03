// // src/lib/firebase/firebase.client.ts
//
// import { initializeApp, getApps, getApp, type FirebaseApp } from "firebase/app";
// import { getAuth, type Auth } from "firebase/auth";
// import { getFirestore, type Firestore } from "firebase/firestore"; // Import Firestore type
//
// const firebaseConfigClient = {
//     apiKey: 'AIzaSyCBaEACR9uDD9ISJ092h2o6y5UzOdY_sJU',
//     authDomain: 'workout-app-441723.firebaseapp.com',
//     projectId: 'workout-app-441723',
//     storageBucket: 'workout-app-441723.appspot.com',
//     messagingSenderId: '209783809936',
//     appId: '1:209783809936:web:fd21752b8673cad1dcb515',
//     measurementId: 'G-RWGLFL9CPN'
// };
//
// let clientApp: FirebaseApp | null = null;
// let clientAuth: Auth | null = null;
// let firestoreDb: Firestore | null = null; // Add Firestore instance
// let isInitialized = false;
//
// // *** THE INITIALIZATION FUNCTION ***
// export function initializeFirebaseClient(): void {
//     if (isInitialized || typeof window === 'undefined') { // Add check for browser environment
//         return; // Prevent double init or server-side run
//     }
//
//     console.log("Attempting Firebase client initialization...");
//
//     try {
//         const appName = 'client-default'; // Use a consistent name
//         const existingApp = getApps().find(app => app.name === appName);
//
//         if (existingApp) {
//             clientApp = existingApp;
//         } else {
//             clientApp = initializeApp(firebaseConfigClient, appName);
//         }
//
//         if (clientApp) {
//             clientAuth = getAuth(clientApp);
//             firestoreDb = getFirestore(clientApp); // Initialize Firestore here too
//             isInitialized = true;
//             console.log("Firebase client initialized successfully.");
//         } else {
//             console.error("Failed to obtain Firebase app instance.");
//             isInitialized = false;
//         }
//
//     } catch (error) {
//         console.error("Firebase client initialization error:", error);
//         clientApp = null;
//         clientAuth = null;
//         firestoreDb = null;
//         isInitialized = false;
//     }
// }
//
// // Getters - return null if not initialized
// export function getClientApp(): FirebaseApp | null { return clientApp; }
// export function getClientAuth(): Auth | null { return clientAuth; }
// export function getDb(): Firestore | null { return firestoreDb; } // Export Firestore getter
// export function isFirebaseClientInitialized(): boolean { return isInitialized; }