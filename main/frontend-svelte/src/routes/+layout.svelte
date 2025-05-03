<script lang="ts">
    import {onMount, setContext} from "svelte";

    let { children } = $props();

    import Footer from "$lib/components/Footer.svelte";
    import Navbar from '$lib/components/Navbar.svelte';
    import "../app.css";
    import {getClientAuth, initializeFirebaseClient,getDb} from "$lib/firebase/firebase.client";
    import {writable} from "svelte/store";
    import { onAuthStateChanged } from 'firebase/auth';
    // Create writable stores
    const userStore = writable(null);
    let isInitialized = false;
    const authStore = writable(null);
    const dbStore = writable(null);
    // Set context for child components
    setContext('user', userStore);
    setContext('auth', authStore);
    setContext('db', dbStore);
    onMount(() => {
            console.log("Initializing Firebase in layout...");
            try {
                // Initialize Firebase client
                initializeFirebaseClient();

                // Get instances and update stores
                const auth = getClientAuth();
                const db = getDb();

                if (auth) {
                    authStore.set(auth);

                    // Set up auth state listener
                    const unsubscribe = onAuthStateChanged(auth, (user) => {
                        console.log("Auth state changed:", user ? "User logged in" : "No user");
                        userStore.set(user);
                    });

                    // Cleanup on component unmount
                    return unsubscribe;
                }

                if (db) {
                    dbStore.set(db);
                }

                isInitialized = true;
            } catch (error) {
                console.error("Error initializing Firebase in layout:", error);
            }

    });
</script>

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
