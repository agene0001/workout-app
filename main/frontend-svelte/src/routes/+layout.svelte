<script lang="ts">
    import { onMount, setContext } from "svelte";
    import { writable, type Writable, get } from "svelte/store"; // Ensure 'get' is imported
    import { createFirebaseReadyStore, type FirebaseReadyState } from "$lib/firebase/firebaseReady";
    import { onAuthStateChanged, type Auth } from 'firebase/auth'; // Ensure Auth and onAuthStateChanged are imported
    import type { Firestore } from 'firebase/firestore'; // Ensure Firestore is imported

    import Footer from "$lib/components/Footer.svelte";
    import Navbar from '$lib/components/Navbar.svelte';
    import "../app.css";
    import { getClientAuth, getDb, initializeFirebaseClient } from "$lib/firebase/firebase.client";

    // Children prop
    let { children } = $props();

    // Create writable stores for Auth and DB instances
    const authStore: Writable<Auth | null> = writable(null);
    const dbStore: Writable<Firestore | null> = writable(null);
    const userStore: Writable<any | null> = writable(null); // Assuming user can be 'any' or null


    // Create the custom firebaseReady store using the Auth and DB stores
    const firebaseReadyStore = createFirebaseReadyStore(authStore, dbStore);

    // Set context for child components
    setContext('auth', authStore);
    setContext('db', dbStore);
    setContext('user', userStore); // Set user store context
    setContext('firebaseReady', firebaseReadyStore); // Provide the new combined ready store


    // State to control initial loading indicator
    // *** Use $state for explicit Svelte 5 reactivity ***
    let isInitialLoading = $state(true); // <-- CHANGE THIS LINE

    // Subscribe to the firebaseReadyStore to update isInitialLoading
    // This subscription happens outside onMount so it's active immediately
    const unsubscribeReady = firebaseReadyStore.subscribe(state => {
        console.log("+layout firebaseReadyStore subscribe:", state);
        if (state.ready) {
            console.log("+layout: Setting isInitialLoading to false.");
            isInitialLoading = false; // <-- Update $state variable
        } else {
            console.log("+layout: Keeping isInitialLoading true.");
            isInitialLoading = true; // <-- Update $state variable
        }
    });


    onMount(() => {
        console.log("+layout onMount starting...");
        let unsubscribeAuth: (() => void) | undefined;

        try {
            // Initialize Firebase client (handles browser check internally)
            // Calling it here ensures it happens after the component mounts,
            // in addition to the sync call on module import (which is guarded).
            initializeFirebaseClient();

            // Get instances from the client module
            const auth = getClientAuth();
            const db = getDb();

            console.log("+layout onMount: getClientAuth returned:", auth);
            console.log("+layout onMount: getDb returned:", db);

            // Set the writable stores with the returned instances
            // These sets will trigger the firebaseReadyStore and its subscribers
            authStore.set(auth);
            dbStore.set(db);

            // Optional: Log store values immediately after setting them to confirm
            console.log("+layout onMount: authStore value after set:", get(authStore));
            console.log("+layout onMount: dbStore value after set:", get(dbStore));


            // Set up auth state listener ONLY if auth instance is available
            // This listener updates the user store and is separate from authStore/dbStore availability
            if (auth) {
                unsubscribeAuth = onAuthStateChanged(auth, (user) => {
                    console.log("Auth state changed:", user ? "User logged in" : "No user");
                    userStore.set(user); // Update the user store
                });
                console.log("+layout onMount: Auth state listener set up.");
            } else {
                console.warn("+layout onMount: Auth instance not available, Auth state listener not set up.");
            }


        } catch (error) {
            console.error("Error initializing Firebase in layout:", error); // <-- Should show if init fails
            // Ensure stores are null on initialization error
            authStore.set(null);
            dbStore.set(null);
            console.log("+layout onMount: Stores set to null after error.");
        }
        console.log("+layout onMount finished.");


        // Return cleanup function that unsubscribes from listeners and stores
        return () => {
            console.log("+layout onMount cleanup running...");
            if (unsubscribeAuth) {
                unsubscribeAuth();
                console.log("+layout onMount cleanup: Auth listener unsubscribed.");
            }
            // Unsubscribe from the firebaseReadyStore subscription created outside onMount
            unsubscribeReady();
            console.log("+layout onMount cleanup: firebaseReadyStore unsubscribed.");
        };
    });
    import { afterNavigate } from '$app/navigation';

    afterNavigate(() => {
        window.gtag('config', 'AW-11461277117');
    });

</script>

{#if isInitialLoading}
    <div class="flex justify-center items-center h-screen bg-zinc-900">
        <p class="text-white text-xl">Loading application essentials...</p>
    </div>
{:else}
    <div class="app">
        <header class="w-full fixed top-0 flex justify-center z-50">
            <div class="max-w-7xl w-full px-4">
                <Navbar />
            </div>
        </header>

        <main>
            {@render children()}
        </main>
        <Footer />
    </div>
{/if}