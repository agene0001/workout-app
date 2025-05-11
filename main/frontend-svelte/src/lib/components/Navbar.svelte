<script>
    import {onMount, getContext} from 'svelte';
    import {
        signInWithEmailAndPassword,
        createUserWithEmailAndPassword,
        signOut,
        // onAuthStateChanged, // No longer needed directly here
        GoogleAuthProvider,
        GithubAuthProvider,
        signInWithPopup
    } from 'firebase/auth';
    // Removed getFirestore import - use the instance from the store
    import {doc, setDoc, getDoc, Timestamp} from 'firebase/firestore';

    // Get the stores from context
    // We now primarily rely on firebaseReadyStore
    const userStore = getContext('user'); // Still need user store for displaying user info
    const firebaseReadyStore = getContext('firebaseReady'); // <-- Get the new store
    // Props
    let name = "";

    // State
    let isMenuOpen = $state(false); // <-- Use $state for Svelte 5 reactivity
    // user is reactive to userStore ($user)
    let user = $state(null);
    let isLoginModalOpen = $state(false);
    let isSignupModalOpen = $state(false);

    let error = $state("");
    let isOperationLoading = $state(false)
    let isAppReady = $state(false); // <-- State derived from firebaseReadyStore
    let fingerprint = $state(null);
    // These are now updated by the firebaseReadyStore subscription
    let currentDb = $state(null); // <-- CHANGE THIS TO $state
    let currentAuth = $state(null); // <-- CHANGE THIS TO $state
    //
    const userfp = 'userfp';
    const userdoc = 'users';

    // FingerprintJS setup
    let fpPromise;
    // Subscribe to the firebaseReadyStore
    const unsubscribeReady = firebaseReadyStore.subscribe(state => {
        // Update local state based on the store's value
        currentAuth = state.auth;
        currentDb = state.db;
        isAppReady = state.ready; // <-- Use the ready flag
        // isInitialLoading can also be derived from isAppReady if needed,
        // but the layout handles the main loading indicator.
    });


    onMount(() => {
        // Cleanup subscriptions
        return () => {
            // Only unsubscribe from the firebaseReadyStore subscription
            unsubscribeReady();
            // The userStore subscription is handled by the reactive declaration ($user)
            // The layout handles the auth state listener cleanup
        };
    });

    onMount(() => {
        // Only import and load FingerprintJS in the browser
        if (typeof window !== 'undefined') {
            import('@fingerprintjs/fingerprintjs').then((FingerprintJS) => {
                fpPromise = FingerprintJS.default.load();
                fpPromise.then(async (fp) => {
                    const result = await fp.get();
                    fingerprint = result.visitorId;
                    console.log("Browser fingerprint loaded:", fingerprint);
                    // No need to call checkAppReady here, the firebaseReadyStore
                    // will update when auth/db are ready. Fingerprint is a separate dependency.
                }).catch(err => {
                    console.error("Error getting fingerprint:", err);
                    error = "Could not get browser fingerprint. Some features might be limited.";
                    fingerprint = 'error'; // Indicate fingerprint failed to load
                });
            }).catch(err => {
                console.error("Error importing fingerprint module:", err);
                error = "Could not load device verification. Please refresh.";
                fingerprint = 'error'; // Indicate fingerprint import failed
            });
        } else {
            // For SSR or non-browser environments, cannot get fingerprint
            fingerprint = 'ssr'; // Indicate fingerprint not available on server
        }
    });

    // *** ADD THIS NEW SUBSCRIPTION FOR THE USER STORE ***
    // Subscribe to the userStore separately to update the local $state(user) variable
    const unsubscribeUser = userStore.subscribe(value => {
        // console.log("userStore subscription received value:", value); // Add log to confirm
        user = value; // <-- Update the local $state(user) variable
    });
    // Authentication providers - only initialize if we have auth available
    // *** ADD THIS $DERIVED DEFINITION HERE INSTEAD ***
    // Use $derived for values computed from $state or other reactive sources
    const providers = $derived(currentAuth ? {
        google: new GoogleAuthProvider(),
        github: new GithubAuthProvider()
    } : {});

    // Helper function for associating fingerprint with user
    // This function now relies on `currentDb` being set by the firebaseReadyStore subscription
    async function associateFingerprintWithUser(userId, fpId) {
        // console.log(`Associating user ${userId} with fingerprint ${fpId}`);
        if (!userId || !fpId) {
            // console.warn("associateFingerprintWithUser called with missing params:", { userId, fpId });
            return;
        }
        // Use the currentDb value from the store subscription
        const db = currentDb;
        if (!db) {
            // This check remains as a safety net, but should not be hit if
            // the calling code (e.g., handleSignupAttempt) is guarded by isAppReady.
            // console.error("associateFingerprintWithUser called before DB instance was available.");
            throw new Error("Database not available for fingerprint association.");
        }
        try {
            const userDocRef = doc(db, userdoc, userId);
            const fpDocRef = doc(db, userfp, fpId);
            const now = Timestamp.now();
            await setDoc(userDocRef, {fingerprint: fpId, lastLogin: now}, {merge: true});
            // console.log(`Successfully updated user doc: ${userDocRef.path}`);

            await setDoc(fpDocRef, {userId: userId, lastSeen: now}, {merge: true});
            // console.log(`Successfully created/updated userfp doc: ${fpDocRef.path}`);
            // console.log(`Successfully associated user ${userId} with fingerprint ${fpId}`);
        } catch (error) {
            // console.error(`Error storing fingerprint ${fpId} for user ${userId}:`, error);
            throw error; // Re-throw to be caught by the caller
        }
    }

    // This function now relies on `currentDb` being set by the firebaseReadyStore subscription
    async function checkExistingFingerprint(fpId) {
        console.log(`Checking fingerprint ID: ${fpId} in Firestore...`);

        // Allow check to proceed if fingerprint is not available (e.g., SSR or error)
        // The calling function (handleSignup/SocialAuth) will handle the implications.
        if (!fpId || fpId === 'error' || fpId === 'ssr') {
            console.warn(`Fingerprint ID not valid or available yet (${fpId}). Cannot perform check.`);
            return null; // Return null if fingerprint isn't usable for a check
        }

        // Use the currentDb value from the store subscription
        const db = currentDb;

        if (!db) {
            // This check remains as a safety net, but should not be hit if
            // the calling code (e.g., handleSignupAttempt) is guarded by isAppReady.
            console.error("checkExistingFingerprint called before DB instance was available.");
            throw new Error("Database not available for fingerprint check.");
        }

        try {
            const docRef = doc(db, userfp, fpId);
            const docSnap = await getDoc(docRef);
            if (docSnap.exists()) {
                const data = docSnap.data();
                console.log(`Fingerprint ${fpId} found, associated userId:`, data.userId);
                return data.userId || null;
            }
            console.log(`Fingerprint ${fpId} not found.`);
            return null;
        } catch (error) {
            console.error(`Error checking fingerprint ${fpId} in Firestore:`, error);
            if (error.code === 'permission-denied') {
                throw new Error("Permission denied checking device status.");
            } else {
                throw new Error(`Error checking device status: ${error.message || 'Unknown error'}`);
            }
        }
    }

    // Auth handlers - Now guarded by isAppReady
    async function handleLoginAttempt(email, password) {
        // Guard this function call with isAppReady check
        if (!isAppReady || isOperationLoading) {
            console.warn("Login attempt blocked: App not ready or operation loading.");
            return false;
        }
        // currentAuth is guaranteed to be non-null if isAppReady is true
        const auth = currentAuth;


        error = "";
        isOperationLoading = true;
        try {
            await signInWithEmailAndPassword(auth, email, password);
            isLoginModalOpen = false;
            return true;
        } catch (err) {
            console.error("Login error:", err);
            if (['auth/user-not-found', 'auth/wrong-password', 'auth/invalid-credential', 'auth/invalid-email'].includes(err.code)) {
                error = "Invalid email or password.";
            } else if (err.code === 'auth/too-many-requests') {
                error = "Too many login attempts. Please try again later.";
            } else {
                error = `Login failed: ${err.message || 'Please try again.'}`;
            }
            return false;
        } finally {
            isOperationLoading = false;
        }
    }

    // Auth handlers - Now guarded by isAppReady
    async function handleSignupAttempt(email, password) {
        // Guard this function call with isAppReady check
        if (!isAppReady || isOperationLoading) {
            console.warn("Signup attempt blocked: App not ready or operation loading.");
            return false;
        }
        // currentAuth is guaranteed to be non-null if isAppReady is true
        const auth = currentAuth;


        error = "";
        isOperationLoading = true;

        // Check for usable fingerprint before proceeding
        if (!fingerprint || fingerprint === 'error' || fingerprint === 'ssr') {
            const fpError = "Device fingerprint not available. Cannot complete signup.";
            console.error(fpError);
            error = fpError;
            isOperationLoading = false;
            return false;
        }

        try {
            // checkExistingFingerprint now uses currentDb (which is set if isAppReady is true)
            console.log("Checking fingerprint before signup...");
            const existingUserId = await checkExistingFingerprint(fingerprint);

            if (existingUserId) {
                const fpExistsError = `This device seems linked to an existing account (User ID starting: ${existingUserId.substring(0, 3)}...). Please log in or contact support.`;
                console.warn(`Signup blocked: Fingerprint ${fingerprint} linked to user ${existingUserId}`);
                error = fpExistsError;
                return false;
            }

            console.log("Fingerprint check passed.");

            // Proceed with signup
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            console.log("Signup successful:", userCredential.user.uid);

            // associateFingerprintWithUser now uses currentDb (which is set if isAppReady is true)
            await associateFingerprintWithUser(userCredential.user.uid, fingerprint);

            isSignupModalOpen = false;
            return true;
        } catch (err) {
            // Catch errors from checkExistingFingerprint or associateFingerprintWithUser
            if (!error) { // Only set a generic error if a specific one wasn't already set
                console.error("Signup process error:", err); // Log the specific error
                error = err.message || "An unexpected error occurred during signup.";
            }
            return false;
        } finally {
            isOperationLoading = false;
        }
    }

    // Auth handlers - Now guarded by isAppReady
    async function handleSocialAuthAttempt(providerKey) {
        // Guard this function call with isAppReady check
        if (!isAppReady || isOperationLoading) {
            console.warn(`${providerKey} attempt blocked: App not ready or operation loading.`);
            return;
        }
        // currentAuth is guaranteed to be non-null if isAppReady is true
        const auth = currentAuth;

        error = "";
        isOperationLoading = true;

        // Check for usable fingerprint before proceeding
        if (!fingerprint || fingerprint === 'error' || fingerprint === 'ssr') {
            const fpError = "Device fingerprint not available. Cannot complete sign-in.";
            console.error(fpError);
            error = fpError;
            isOperationLoading = false;
            return;
        }


        const socialProvider = providers[providerKey];
        if (!socialProvider) {
            error = `Invalid social provider: ${providerKey}`;
            isOperationLoading = false;
            return;
        }

        try {
            // checkExistingFingerprint now uses currentDb (which is set if isAppReady is true)
            console.log(`Checking fingerprint before ${providerKey} sign-in...`);
            const existingUserId = await checkExistingFingerprint(fingerprint);
            if (existingUserId) {
                const fpExistsError = `This device seems linked to an existing account (User ID starting: ${existingUserId.substring(0, 6)}). Please log in or contact support.`;
                console.warn(`${providerKey} sign-in blocked: Fingerprint ${fingerprint} linked to user ${existingUserId}`);
                error = fpExistsError;
                throw new Error(fpExistsError); // Throw to be caught below
            }

            console.log("Fingerprint check passed.");

            // Proceed with social sign in
            const userCredential = await signInWithPopup(auth, socialProvider);
            console.log(`${providerKey} sign-in successful:`, userCredential.user.uid);

            // associateFingerprintWithUser now uses currentDb (which is set if isAppReady is true)
            await associateFingerprintWithUser(userCredential.user.uid, fingerprint);

            // Close modals on success
            isLoginModalOpen = false;
            isSignupModalOpen = false;
        } catch (err) {
            if (!error) {
                console.error(`${providerKey} auth error:`, err);
                if (err.code === 'auth/account-exists-with-different-credential') {
                    error = "Account exists with this email but a different sign-in method.";
                } else if (['auth/popup-closed-by-user', 'auth/cancelled-popup-request'].includes(err.code)) {
                    error = "Sign-in popup was closed or cancelled.";
                } else {
                    error = `Sign-in failed: ${err.message || 'Please try again.'}`;
                }
            }
        } finally {
            isOperationLoading = false;
        }
    }

    async function handleLogout() {
        // Logout doesn't strictly require DB, but checking auth is available is good
        if (isOperationLoading) {
            console.warn("Logout attempt blocked: Operation loading.");
            return;
        }
        // currentAuth is available if isAppReady is true, but logout might be needed
        // even if DB isn't ready. Let's just check currentAuth directly.
        const auth = currentAuth;
        if (!auth) {
            console.warn("Logout attempted but auth service not available.");
            return;
        }

        error = "";
        try {
            await signOut(auth);
            console.log("User signed out");
        } catch (err) {
            console.error("Error signing out:", err);
            error = "Failed to sign out. Please try again.";
        }
    }


    // Modal control functions (no changes needed here)
    function openLoginModal() {
        // Only open if app is ready
        if (isAppReady) {
            error = '';
            isSignupModalOpen = false;
            isLoginModalOpen = true;
        } else {
            console.warn("Attempted to open login modal before app ready.");
        }
    }

    function openSignupModal() {
        // Only open if app is ready
        if (isAppReady) {
            error = '';
            isLoginModalOpen = false;
            isSignupModalOpen = true;
        } else {
            console.warn("Attempted to open signup modal before app ready.");
        }
    }

    function closeLoginModal() {
        isLoginModalOpen = false;
    }

    function closeSignupModal() {
        isSignupModalOpen = false;
    }

    function switchToSignup() {
        // Only switch if app is ready
        if (isAppReady) {
            closeLoginModal();
            openSignupModal();
        }
    }

    function switchToLogin() {
        // Only switch if app is ready
        if (isAppReady) {
            closeSignupModal();
            openLoginModal();
        }
    }

</script>


<header class="relative px-4 py-2">
    <nav class="bg-zinc-900 text-danger sticky top-0 shadow-md rounded-2xl py-3 z-40">
        <div class="container mx-auto px-4">
            <div class="flex items-center justify-between">
                <div class="flex items-center flex-shrink-0">
                    <button on:click={isMenuOpen=false}>    <a href="/"
                       class="text-3xl lg:text-4xl font-orbital flex items-center font-bold px-2 py-2 text-[#00dd87]">
                        <img src="/imgs/gainztrackersfavicon.png" alt="Gains Trackers Logo"
                             class="mr-2 text-sm h-8 lg:h-10 w-auto"/>
                        Gains Tracker
                    </a></button>
                    <ul class="hidden lg:flex items-center ml-6">
                        <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform text-[#00dd87] hover:text-secondary">
                            <button on:click={isMenuOpen=false}>   <a class={name.toLowerCase() === "nutrition" ? "text-info font-bold" : ""}
                                                                      href="/Nutrition">Nutrition</a></button>
                        </li>
                        <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform text-[#00dd87] hover:text-secondary">
                            <button on:click={isMenuOpen=false}>      <a class={name.toLowerCase() === "about-us" ? "text-info font-bold" : ""} href="/About-Us">About
                                Us</a></button>
                        </li>
                        <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform text-[#00dd87] hover:text-secondary">
                            <button on:click={isMenuOpen=false}>   <a class={name.toLowerCase() === "blog" ? "text-info font-bold" : ""} href="/Blog">Blog</a></button>
                        </li>
                    </ul>
                </div>

                <div class="hidden lg:flex items-center gap-3 flex-shrink-0">
                    {#if user}
                        <div class="flex items-center gap-3">
            <span class="text-green-400 text-sm lg:text-base truncate max-w-[150px] lg:max-w-[250px]"
                  title={user.email || user.displayName || 'User'}>
              Hello, {user.displayName || (user.email ? user.email.split('@')[0] : "User")}
            </span>
                            <button
                                    class="border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white px-3 lg:px-4 py-1.5 lg:py-2 rounded-md transition-all text-sm lg:text-base"
                                    on:click={handleLogout}>
                                Logout
                            </button>
                        </div>
                    {:else}
                        <button
                                class="border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-3 lg:px-4 py-1.5 lg:py-2 rounded-md transition-all text-sm lg:text-base disabled:opacity-50 disabled:cursor-not-allowed"
                                on:click={openLoginModal}
                                disabled={!isAppReady}>
                            Login
                        </button>
                        <button
                                class="bg-green-500 text-white hover:bg-green-600 px-3 lg:px-4 py-1.5 lg:py-2 rounded-md transition-all text-sm lg:text-base disabled:opacity-50 disabled:cursor-not-allowed"
                                on:click={openSignupModal}
                                disabled={!isAppReady}>
                            Sign Up
                        </button>
                    {/if}
                </div>

                <button
                        class="lg:hidden block text-gray-300 hover:text-white p-2"
                        type="button" on:click={() => isMenuOpen = !isMenuOpen} aria-label="Toggle menu"
                        aria-expanded={isMenuOpen}>
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        {#if isMenuOpen}
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M6 18L18 6M6 6l12 12"/>
                        {:else}
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M4 6h16M4 12h16M4 18h16"/>
                        {/if}
                    </svg>
                </button>
            </div>

            <div class="lg:hidden overflow-hidden transition-all duration-300 ease-in-out {isMenuOpen ? 'max-h-screen mt-4 opacity-100' : 'max-h-0 mt-0 opacity-0'}">
                <ul class="flex flex-col items-center border-t border-zinc-700 pt-4">
                    <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform">
                        <button on:click={isMenuOpen=false}>   <a class={name.toLowerCase() === "nutrition" ? "text-white font-bold underline" : "text-green-500"}
                           href="/Nutrition">Nutrition</a>
                        </button>
                    </li>

                    <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform">
                        <button on:click={isMenuOpen=false}>    <a class={name.toLowerCase() === "about-us" ? "text-white font-bold underline" : "text-green-500"}
                                                                   href="/About-Us">About Us</a></button>
                    </li>
                    <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform">
                       <button on:click={isMenuOpen=false}> <a class={name.toLowerCase() === "blog" ? "text-white font-bold underline" : "text-green-500"}
                           href="/Blog">Blog</a>
                       </button>
                    </li>
                </ul>

                <div class="mt-4 pt-4 border-t border-zinc-700 flex flex-col items-center gap-3 px-4 pb-4">
                    {#if user}
                        <div class="flex flex-col items-center gap-3 w-full max-w-xs">
            <span class="text-green-400 text-center truncate w-full"
                  title={user.email || user.displayName || 'User'}>
              Hello, {user.displayName || (user.email ? user.email.split('@')[0] : "User")}
            </span>
                            <button
                                    class="w-full border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white px-4 py-2 rounded-md transition-all"
                                    on:click={handleLogout}>
                                Logout
                            </button>
                        </div>
                    {:else}
                        <button
                                class="w-full max-w-xs border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-4 py-2 rounded-md transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                                on:click={() => { isMenuOpen = false; openLoginModal(); }}
                                disabled={!isAppReady}>
                            Login
                        </button>
                        <button
                                class="w-full max-w-xs bg-green-500 text-white hover:bg-green-600 px-4 py-2 rounded-md transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                                on:click={() => { isMenuOpen = false; openSignupModal(); }}
                                disabled={!isAppReady}>
                            Sign Up
                        </button>
                    {/if}
                </div>
            </div>
        </div>
    </nav>

    {#if isLoginModalOpen}
        <div
                class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center transition-opacity duration-300"
                on:click={closeLoginModal}
        >
            <div
                    class="bg-zinc-800 p-6 rounded-lg w-full max-w-md shadow-xl transform transition-all duration-300 animate-fade-in-scale"
                    on:click|stopPropagation
            >
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-2xl font-bold text-white">Login</h2>
                    <button on:click={closeLoginModal} class="text-gray-400 hover:text-white transition-colors"
                            aria-label="Close modal">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>

                <form on:submit|preventDefault={() => {
                    const emailInput = document.querySelector('#login-email');
                    const passwordInput = document.querySelector('#login-password');
                    // Check isAppReady and isOperationLoading before calling handler
                    if(isAppReady && !isOperationLoading) {
                        handleLoginAttempt(emailInput.value, passwordInput.value);
                    }
                }}>
                    <div class="mb-4">
                        <label for="login-email" class="block text-gray-300 mb-2">Email</label>
                        <input
                                type="email"
                                id="login-email"
                                class="w-full bg-zinc-700 text-white px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                placeholder="your@email.com"
                                required
                        />
                    </div>
                    <div class="mb-4">
                        <label for="login-password" class="block text-gray-300 mb-2">Password</label>
                        <input
                                type="password"
                                id="login-password"
                                class="w-full bg-zinc-700 text-white px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                placeholder="••••••••"
                                required
                        />
                    </div>

                    {#if error}
                        <div class="navbar-error-container text-red-500" role="alert">
                            <p class="error-message">{error}</p>
                            <button on:click={() => error = ''} aria-label="Dismiss error message" class="dismiss-button">
                                &times;
                            </button>
                        </div>
                    {/if}

                    <button
                            type="submit"
                            class="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            disabled={isOperationLoading || !isAppReady}>
                        {isOperationLoading ? 'Logging in...' : 'Login'}
                    </button>
                </form>

                <div class="mt-4 text-center">
                    <p class="text-gray-400">or login with</p>
                    <div class="flex justify-center mt-2 space-x-4">
                        <button
                                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                                on:click={() => isAppReady && !isOperationLoading && handleSocialAuthAttempt('google')}
                                disabled={isOperationLoading || !isAppReady}>
                            Google
                        </button>
                        <button
                                class="bg-gray-800 text-white px-4 py-2 rounded-md hover:bg-gray-900 transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                                on:click={() => isAppReady && !isOperationLoading && handleSocialAuthAttempt('github')}
                                disabled={isOperationLoading || !isAppReady}>
                            GitHub
                        </button>
                    </div>
                </div>

                <div class="mt-6 text-center">
                    <p class="text-gray-400">
                        Don't have an account?
                        <button on:click={switchToSignup}
                                class="text-green-400 hover:underline disabled:opacity-50 disabled:cursor-not-allowed"
                                disabled={!isAppReady}>Sign Up
                        </button>
                    </p>
                </div>
            </div>
        </div>
        <style>
            @keyframes fade-in-scale {
                from {
                    opacity: 0;
                    transform: scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }

            .animate-fade-in-scale {
                animation: fade-in-scale 0.3s ease-out forwards;
            }
        </style>
    {/if}

    {#if isSignupModalOpen}
        <div
                class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center transition-opacity duration-300"
                on:click={closeSignupModal}
        >
            <div
                    class="bg-zinc-800 p-6 rounded-lg w-full max-w-md shadow-xl transform transition-all duration-300 animate-fade-in-scale"
                    on:click|stopPropagation
            >
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-2xl font-bold text-white">Create Account</h2>
                    <button on:click={closeSignupModal} class="text-gray-400 hover:text-white transition-colors"
                            aria-label="Close modal">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>

                <form on:submit|preventDefault={() => {
                    const emailInput = document.querySelector('#signup-email');
                    const passwordInput = document.querySelector('#signup-password');
                     // Check isAppReady and isOperationLoading before calling handler
                    if(isAppReady && !isOperationLoading) {
                         handleSignupAttempt(emailInput.value, passwordInput.value);
                    }
                }}>
                    <div class="mb-4">
                        <label for="signup-email" class="block text-gray-300 mb-2">Email</label>
                        <input
                                type="email"
                                id="signup-email"
                                class="w-full bg-zinc-700 text-white px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                placeholder="your@email.com"
                                required
                        />
                    </div>
                    <div class="mb-4">
                        <label for="signup-password" class="block text-gray-300 mb-2">Password</label>
                        <input
                                type="password"
                                id="signup-password"
                                class="w-full bg-zinc-700 text-white px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                placeholder="••••••••"
                                required
                        />
                    </div>

                    {#if error}
                        <div class="text-red-500 navbar-error-container" role="alert">
                            <p class="error-message">{error}</p>
                            <button on:click={() => error = ''} aria-label="Dismiss error message" class="dismiss-button">
                                &times;
                            </button>
                        </div>
                    {/if}

                    <button
                            type="submit"
                            class="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            disabled={isOperationLoading || !isAppReady}>
                        {isOperationLoading ? 'Creating account...' : 'Sign Up'}
                    </button>
                </form>

                <div class="mt-4 text-center">
                    <p class="text-gray-400">or sign up with</p>
                    <div class="flex justify-center mt-2 space-x-4">
                        <button
                                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                                on:click={() => isAppReady && !isOperationLoading && handleSocialAuthAttempt('google')}
                                disabled={isOperationLoading || !isAppReady}>
                            Google
                        </button>
                        <button
                                class="bg-gray-800 text-white px-4 py-2 rounded-md hover:bg-gray-900 transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                                on:click={() => isAppReady && !isOperationLoading && handleSocialAuthAttempt('github')}
                                disabled={isOperationLoading || !isAppReady}>
                            GitHub
                        </button>
                    </div>
                </div>

                <div class="mt-6 text-center">
                    <p class="text-gray-400">
                        Already have an account?
                        <button on:click={switchToLogin}
                                class="text-green-400 hover:underline disabled:opacity-50 disabled:cursor-not-allowed"
                                disabled={!isAppReady}>Login
                        </button>
                    </p>
                </div>
            </div>
        </div>
    {/if}
</header>
