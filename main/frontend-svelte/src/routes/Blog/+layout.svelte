<script>
    import { onMount, setContext } from 'svelte';
    import { initializeFirebaseClient, isAdmin, isInitialized } from '$lib/firebase/firebase.client';

    // Make these stores available to all child components via context
    setContext('isAdmin', isAdmin);
    setContext('isInitialized', isInitialized);

    // Initialize Firebase on mount
    onMount(async () => {
        await initializeFirebaseClient();
    });
</script>

<slot />