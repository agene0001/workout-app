// src/lib/stores/firebaseReady.ts
import { derived, type Readable, type Writable, get } from 'svelte/store'; // Import get if needed for direct reads, derived imports it implicitly
import type { Auth } from 'firebase/auth';
import type { Firestore } from 'firebase/firestore';
import { browser } from '$app/environment';

export interface FirebaseReadyState {
    auth: Auth | null;
    db: Firestore | null;
    ready: boolean;
}

export function createFirebaseReadyStore(
    authStore: Writable<Auth | null>,
    dbStore: Writable<Firestore | null>
): Readable<FirebaseReadyState> {
    const firebaseReady = derived(
        [authStore, dbStore],
        ([$auth, $db], set) => {
            // This callback runs whenever authStore or dbStore changes
            console.log("firebaseReadyStore derived: Received auth:", $auth, "db:", $db); // <-- ADD THIS LOG
            console.log("firebaseReadyStore derived: auth !== null:", $auth !== null, "db !== null:", $db !== null); // <-- ADD THIS LOG

            if (!browser) {
                set({ auth: null, db: null, ready: false });
                return;
            }

            const isReady = $auth !== null && $db !== null;

            console.log("firebaseReadyStore derived: isReady calculated as:", isReady); // <-- ADD THIS LOG

            set({
                auth: $auth,
                db: $db,
                ready: isReady
            });
        },
        { auth: null, db: null, ready: false } as FirebaseReadyState
    );

    return firebaseReady;
}