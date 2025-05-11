<script>
    import { onMount, setContext } from 'svelte';
    import { getClientAuth, checkIsUserAdmin } from '$lib/firebase/firebase.client';
    import {getIdTokenResult, onAuthStateChanged} from 'firebase/auth';
    import { writable } from "svelte/store";

    // Create stores at the layout level
    export const isAdmin = writable(checkIsUserAdmin());
    // const isAdminChecked = writable(false);

    // Make these stores available to all child components via context
    setContext('isAdmin', isAdmin);
    // Initialize Firebase auth
    const auth = getClientAuth();


</script>

<slot />