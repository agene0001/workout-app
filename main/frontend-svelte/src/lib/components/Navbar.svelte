<script>
    import { onMount, getContext } from 'svelte';
    import {
        signInWithEmailAndPassword,
        createUserWithEmailAndPassword,
        signOut,
        onAuthStateChanged,
        GoogleAuthProvider,
        GithubAuthProvider,
        signInWithPopup
    } from 'firebase/auth';
    import { doc, setDoc, getDoc, Timestamp } from 'firebase/firestore';

    // Get stores from context with safety checks
    const authStore = getContext('auth') || { subscribe: () => () => {} };
    const dbStore = getContext('db') || { subscribe: () => () => {} };
    const userStore = getContext('user') || { subscribe: () => () => {} };

    // Props
    export let name = "";

    // State
    let isMenuOpen = false;
    let user = null;
    let isLoginModalOpen = false;
    let isSignupModalOpen = false;
    let error = "";
    let isOperationLoading = false;
    let isInitialLoading = true;
    let fingerprint = null;
    let currentDb = null; // Local variable for db instance
    let currentAuth = null; // Local variable for auth instance

    // Safe subscriptions with fallbacks
    $: user = $userStore;

    const unsubDb = dbStore.subscribe(value => {
        currentDb = value;
        if (value) console.log("DB store value received");
    });

    const unsubAuth = authStore.subscribe(value => {
        currentAuth = value;
        if (value) console.log("Auth store value received");
    });

    const userfp = 'userfp';
    const userdoc = 'users';

    // FingerprintJS setup
    let fpPromise;

    onMount(() => {
        // Cleanup subscriptions
        return () => {
            unsubDb();
            unsubAuth();
        };
    });

    onMount(() => {
        // Only import and load FingerprintJS in the browser
        if (typeof window !== 'undefined') {
            import('@fingerprintjs/fingerprintjs').then((FingerprintJS) => {
                fpPromise = FingerprintJS.default.load();
                // Continue with fingerprint logic here...
                fpPromise.then(async (fp) => {
                    const result = await fp.get();
                    fingerprint = result.visitorId;
                    console.log("Browser fingerprint loaded:", fingerprint);

                    // Complete loading after fingerprint is obtained
                    isInitialLoading = false;
                }).catch(err => {
                    console.error("Error getting fingerprint:", err);
                    error = "Could not get browser fingerprint. Some features might be limited.";
                    isInitialLoading = false;
                });
            }).catch(err => {
                console.error("Error importing fingerprint module:", err);
                isInitialLoading = false;
            });
        } else {
            isInitialLoading = false;
        }
    });

    // Authentication providers - only initialize if we have auth available
    $: providers = currentAuth ? {
        google: new GoogleAuthProvider(),
        github: new GithubAuthProvider()
    } : {};

    // Helper function for associating fingerprint with user
    async function associateFingerprintWithUser(userId, fpId) {
        console.log(`Associating user ${userId} with fingerprint ${fpId}`);
        if (!userId || !fpId || !currentDb) return;
        try {
            const now = Timestamp.now();
            await setDoc(doc(currentDb, userdoc, userId), { fingerprint: fpId, lastLogin: now }, { merge: true });
            await setDoc(doc(currentDb, userfp, fpId), { userId: userId, lastSeen: now }, { merge: true });
            console.log(`Successfully associated user ${userId} with fingerprint ${fpId}`);
        } catch (error) {
            console.error(`Error storing fingerprint ${fpId} for user ${userId}:`, error);
        }
    }

    async function checkExistingFingerprint(fpId) {
        console.log(`Checking fingerprint ID: ${fpId} in Firestore...`);
        if (!fpId || !currentDb) return null;
        try {
            const docRef = doc(currentDb, userfp, fpId);
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
                error = "Error checking device status (permissions).";
            } else {
                error = "Error checking device status.";
            }
            throw error;
        }
    }

    // Auth handlers - Check if auth is available
    async function handleLoginAttempt(email, password) {
        if (!currentAuth) {
            error = "Authentication service not available";
            return false;
        }

        error = "";
        isOperationLoading = true;
        try {
            await signInWithEmailAndPassword(currentAuth, email, password);
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

    async function handleSignupAttempt(email, password) {
        if (!currentAuth) {
            error = "Authentication service not available";
            return false;
        }

        error = "";
        isOperationLoading = true;

        if (!fingerprint) {
            error = "Could not verify device fingerprint. Please refresh and try again.";
            isOperationLoading = false;
            return false;
        }

        try {
            // Check fingerprint first
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
            const userCredential = await createUserWithEmailAndPassword(currentAuth, email, password);
            console.log("Signup successful:", userCredential.user.uid);

            // Associate fingerprint
            await associateFingerprintWithUser(userCredential.user.uid, fingerprint);

            isSignupModalOpen = false;
            return true;
        } catch (err) {
            if (!error) {
                console.error("Signup error:", err);
                if (err.code === 'auth/email-already-in-use') {
                    error = "This email is already registered. Please log in.";
                } else if (err.code === 'auth/weak-password') {
                    error = "Password is too weak (min. 6 characters).";
                } else if (err.code === 'auth/invalid-email') {
                    error = "Please enter a valid email address.";
                } else {
                    error = `Signup failed: ${err.message || 'Please try again.'}`;
                }
            }
            return false;
        } finally {
            isOperationLoading = false;
        }
    }

    async function handleSocialAuthAttempt(providerKey) {
        if (!currentAuth) {
            error = "Authentication service not available";
            return;
        }

        error = "";
        isOperationLoading = true;

        if (!fingerprint) {
            error = "Could not verify device fingerprint. Please refresh and try again.";
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
            // Check fingerprint first
            console.log(`Checking fingerprint before ${providerKey} sign-in...`);
            const existingUserId = await checkExistingFingerprint(fingerprint);
            if (existingUserId) {
                const fpExistsError = `This device seems linked to an existing account (User ID starting: ${existingUserId.substring(0, 6)}). Please log in or contact support.`;
                console.warn(`${providerKey} sign-in blocked: Fingerprint ${fingerprint} linked to user ${existingUserId}`);
                error = fpExistsError;
                throw new Error(fpExistsError);
            }

            console.log("Fingerprint check passed.");

            // Proceed with social sign in
            const userCredential = await signInWithPopup(currentAuth, socialProvider);
            console.log(`${providerKey} sign-in successful:`, userCredential.user.uid);

            // Associate fingerprint
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
        if (!currentAuth) {
            error = "Authentication service not available";
            return;
        }

        error = "";
        try {
            await signOut(currentAuth);
            console.log("User signed out");
        } catch (err) {
            console.error("Error signing out:", err);
            error = "Failed to sign out. Please try again.";
        }
    }

    // Modal control functions
    function openLoginModal() {
        error = '';
        isSignupModalOpen = false;
        isLoginModalOpen = true;
    }

    function openSignupModal() {
        error = '';
        isLoginModalOpen = false;
        isSignupModalOpen = true;
    }

    function closeLoginModal() {
        isLoginModalOpen = false;
    }

    function closeSignupModal() {
        isSignupModalOpen = false;
    }

    function switchToSignup() {
        closeLoginModal();
        openSignupModal();
    }

    function switchToLogin() {
        closeSignupModal();
        openLoginModal();
    }
    //
    // onMount(async () => {
    //     if (!currentAuth) {
    //         console.warn("Authentication is not available in Navbar component");
    //     }
    //
    //     try {
    //         // Only proceed if fingerprint promise is available
    //         if (fpPromise) {
    //             // Load fingerprint
    //             const fp = await fpPromise;
    //             const result = await fp.get();
    //             fingerprint = result.visitorId;
    //             console.log("Browser fingerprint loaded:", fingerprint);
    //
    //             // Associate fingerprint if user is logged in
    //             if (user && fingerprint) {
    //                 associateFingerprintWithUser(user.uid, fingerprint).catch(err =>
    //                     console.error("Failed background fingerprint association:", err)
    //                 );
    //             }
    //         }
    //     } catch (err) {
    //         console.error("Error getting fingerprint:", err);
    //         error = "Could not get browser fingerprint. Some features might be limited.";
    //     }
    //
    //     // Complete initial loading
    //     isInitialLoading = false;
    // });
</script>


{#if isInitialLoading}
    <div class="flex justify-center items-center h-screen bg-zinc-900">
        <p class="text-white text-xl">Initializing...</p>
    </div>
{:else}
    <header class="relative px-4 py-2">
        <nav class="bg-zinc-900 text-danger sticky top-0 shadow-md rounded-2xl py-3 z-40">
            <div class="container mx-auto px-4">
                <div class="flex items-center justify-between">
                    <!-- Logo/Brand and Desktop Navigation -->
                    <div class="flex items-center flex-shrink-0">
                        <a href="/" class="text-3xl lg:text-4xl font-orbital flex items-center font-bold px-2 py-2 text-[#00dd87]">
                            <img src="/imgs/gainztrackersfavicon.png" alt="Gains Trackers Logo" class="mr-2 text-sm h-8 lg:h-10 w-auto"/>
                            Gains Tracker
                        </a>
                        <ul class="hidden lg:flex items-center ml-6">
                            <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform text-[#00dd87] hover:text-secondary">
                                <a class={name.toLowerCase() === "nutrition" ? "text-info font-bold" : ""} href="/Nutrition">Nutrition</a>
                            </li>
<!--                            <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform text-[#00dd87] hover:text-secondary">-->
<!--                                <a class={name.toLowerCase() === "groups" ? "text-info font-bold" : ""} href="/Groups">Workout Groups</a>-->
<!--                            </li>-->
                            <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform text-[#00dd87] hover:text-secondary">
                                <a class={name.toLowerCase() === "about-us" ? "text-info font-bold" : ""} href="/About-Us">About Us</a>
                            </li>
                            <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform text-[#00dd87] hover:text-secondary">
                                <a class={name.toLowerCase() === "blog" ? "text-info font-bold" : ""} href="/Blog">Blog</a>
                            </li>
                        </ul>
                    </div>

                    <!-- Authentication Buttons (Desktop) -->
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
                                    class="border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-3 lg:px-4 py-1.5 lg:py-2 rounded-md transition-all text-sm lg:text-base"
                                    on:click={openLoginModal}>
                                Login
                            </button>
                            <button
                                    class="bg-green-500 text-white hover:bg-green-600 px-3 lg:px-4 py-1.5 lg:py-2 rounded-md transition-all text-sm lg:text-base"
                                    on:click={openSignupModal}>
                                Sign Up
                            </button>
                        {/if}
                    </div>

                    <!-- Mobile menu button -->
                    <button
                            class="lg:hidden block text-gray-300 hover:text-white p-2"
                            type="button" on:click={() => isMenuOpen = !isMenuOpen} aria-label="Toggle menu" aria-expanded={isMenuOpen}>
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            {#if isMenuOpen}
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            {:else}
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                            {/if}
                        </svg>
                    </button>
                </div>

                <!-- Mobile Navigation Menu -->
                <div class="lg:hidden overflow-hidden transition-all duration-300 ease-in-out {isMenuOpen ? 'max-h-screen mt-4 opacity-100' : 'max-h-0 mt-0 opacity-0'}">
                    <ul class="flex flex-col items-center border-t border-zinc-700 pt-4">
                        <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform">
                            <a class={name.toLowerCase() === "nutrition" ? "text-white font-bold underline" : "text-green-500"} href="/Nutrition">Nutrition</a>
                        </li>
                        <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform">
                            <a class={name.toLowerCase() === "groups" ? "text-white font-bold underline" : "text-green-500"} href="/Groups">Workout Groups</a>
                        </li>
                        <li class="text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform">
                            <a class={name.toLowerCase() === "about-us" ? "text-white font-bold underline" : "text-green-500"} href="/About-Us">About Us</a>
                        </li>
                    </ul>

                    <!-- Mobile Authentication Buttons -->
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
                                    class="w-full max-w-xs border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-4 py-2 rounded-md transition-all"
                                    on:click={() => { isMenuOpen = false; openLoginModal(); }}>
                                Login
                            </button>
                            <button
                                    class="w-full max-w-xs bg-green-500 text-white hover:bg-green-600 px-4 py-2 rounded-md transition-all"
                                    on:click={() => { isMenuOpen = false; openSignupModal(); }}>
                                Sign Up
                            </button>
                        {/if}
                    </div>
                </div>
            </div>
        </nav>

        <!-- Login Modal -->
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
                        <button on:click={closeLoginModal} class="text-gray-400 hover:text-white transition-colors" aria-label="Close modal">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>

                    <!-- Login Form -->
                    <form on:submit|preventDefault={() => {
            const emailInput = document.querySelector('#login-email');
            const passwordInput = document.querySelector('#login-password');
            handleLoginAttempt(emailInput.value, passwordInput.value);
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
                            <div class="mb-4 text-red-500 text-sm">{error}</div>
                        {/if}

                        <button
                                type="submit"
                                class="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                disabled={isOperationLoading}
                        >
                            {isOperationLoading ? 'Logging in...' : 'Login'}
                        </button>
                    </form>

                    <div class="mt-4 text-center">
                        <p class="text-gray-400">or login with</p>
                        <div class="flex justify-center mt-2 space-x-4">
                            <button
                                    class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center"
                                    on:click={() => handleSocialAuthAttempt('google')}
                                    disabled={isOperationLoading}
                            >
                                Google
                            </button>
                            <button
                                    class="bg-gray-800 text-white px-4 py-2 rounded-md hover:bg-gray-900 transition-colors flex items-center"
                                    on:click={() => handleSocialAuthAttempt('github')}
                                    disabled={isOperationLoading}
                            >
                                GitHub
                            </button>
                        </div>
                    </div>

                    <div class="mt-6 text-center">
                        <p class="text-gray-400">
                            Don't have an account?
                            <button on:click={switchToSignup} class="text-green-400 hover:underline">Sign Up</button>
                        </p>
                    </div>
                </div>
            </div>
            <style>
                @keyframes fade-in-scale {
                    from { opacity: 0; transform: scale(0.95); }
                    to { opacity: 1; transform: scale(1); }
                }
                .animate-fade-in-scale { animation: fade-in-scale 0.3s ease-out forwards; }
            </style>
        {/if}

        <!-- Signup Modal -->
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
                        <button on:click={closeSignupModal} class="text-gray-400 hover:text-white transition-colors" aria-label="Close modal">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>

                    <!-- Signup Form -->
                    <form on:submit|preventDefault={() => {
            const emailInput = document.querySelector('#signup-email');
            const passwordInput = document.querySelector('#signup-password');
            handleSignupAttempt(emailInput.value, passwordInput.value);
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
                            <div class="mb-4 text-red-500 text-sm">{error}</div>
                        {/if}

                        <button
                                type="submit"
                                class="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                disabled={isOperationLoading}
                        >
                            {isOperationLoading ? 'Creating account...' : 'Sign Up'}
                        </button>
                    </form>

                    <div class="mt-4 text-center">
                        <p class="text-gray-400">or sign up with</p>
                        <div class="flex justify-center mt-2 space-x-4">
                            <button
                                    class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center"
                                    on:click={() => handleSocialAuthAttempt('google')}
                                    disabled={isOperationLoading}
                            >
                                Google
                            </button>
                            <button
                                    class="bg-gray-800 text-white px-4 py-2 rounded-md hover:bg-gray-900 transition-colors flex items-center"
                                    on:click={() => handleSocialAuthAttempt('github')}
                                    disabled={isOperationLoading}
                            >
                                GitHub
                            </button>
                        </div>
                    </div>

                    <div class="mt-6 text-center">
                        <p class="text-gray-400">
                            Already have an account?
                            <button on:click={switchToLogin} class="text-green-400 hover:underline">Login</button>
                        </p>
                    </div>
                </div>
            </div>
        {/if}
    </header>
{/if}