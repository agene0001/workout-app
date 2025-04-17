"use client";
import React, { useState, useEffect, useCallback } from "react"; // Added useCallback
import { NavItemProps } from "../types";
import {
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
    User,
    GoogleAuthProvider,
    GithubAuthProvider,
    signInWithPopup,
    AuthError // Import AuthError for better type checking
} from "firebase/auth";
import { auth } from "../firebase/config";
import app from "../firebase/config";
import { getFunctions, httpsCallable } from "firebase/functions";
import FingerprintJS from '@fingerprintjs/fingerprintjs';

// --- Import the new form components ---
import { LoginForm } from "./LoginForm";   // Adjust path if necessary
import { SignupForm } from "./SignupForm"; // Adjust path if necessary

const functions = getFunctions(app);
const associateFingerprint = httpsCallable(functions, 'associateFingerprint');
const checkFingerprintExists = httpsCallable(functions, 'checkFingerprintExists');


const fpPromise = FingerprintJS.load();

// Modal component (Keep as is from your code)
const Modal = React.memo(({isOpen, onClose, title, children}: {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode
}) => {
    if (!isOpen) return null;
    const handleModalContentClick = (e: React.MouseEvent) => e.stopPropagation();
    return (<div
        className="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center transition-opacity duration-300"
        onClick={onClose}
    >
        <div
            className="bg-zinc-800 p-6 rounded-lg w-full max-w-md shadow-xl transform transition-all duration-300 scale-95 opacity-0 animate-fade-in-scale"
            onClick={handleModalContentClick}
        >
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-white">{title}</h2>
                <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors" aria-label="Close modal">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
            </div>
            {children}
        </div>
        <style>{`
          @keyframes fade-in-scale {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
          }
          .animate-fade-in-scale { animation: fade-in-scale 0.3s ease-out forwards; }
        `}</style>
    </div>);
});
Modal.displayName = "Modal";

// Authentication providers configuration
const providers = {
    google: new GoogleAuthProvider(),
    github: new GithubAuthProvider(),
};

// NavItem component (Keep as is from your code)
const NavItem: React.FC<NavItemProps> = ({ text }) => {
    const [isHovered, setIsHovered] = useState(false);
    return (
        <li
            className={`text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ease-in-out transform ${isHovered ? "text-secondary scale-105" : "text-[#00dd87] hover:text-secondary"}`}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            {text}
        </li>
    );
};

function Navbar(props: { name: string }) {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [user, setUser] = useState<User | null>(null);
    const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
    const [isSignupModalOpen, setIsSignupModalOpen] = useState(false);
    // --- REMOVED email, password state ---
    const [error, setError] = useState(""); // For displaying errors (can be set by handlers)
    const [isOperationLoading, setIsOperationLoading] = useState(false); // Renamed for clarity - controls loading state for auth actions
    const [isInitialLoading, setIsInitialLoading] = useState(true); // Tracks initial fingerprint/auth check
    const [fingerprint, setFingerprint] = useState<string | null>(null);

    // --- Fingerprint and Auth State Effects (Keep similar logic) ---
    useEffect(() => {
        let isMounted = true;
        const getFingerprint = async () => {
            try {
                const fp = await fpPromise;
                const result = await fp.get();
                if (isMounted) {
                    setFingerprint(result.visitorId);
                    console.log("Browser fingerprint loaded:", result.visitorId);
                }
            } catch (error) {
                console.error("Error getting fingerprint:", error);
                if (isMounted) {
                    setError("Could not get browser fingerprint. Some features might be limited.");
                }
            } finally {
                // Check if auth state is already known to potentially finish initial loading
                if (isMounted && auth.currentUser !== undefined) { // Check if onAuthStateChanged already ran
                    setIsInitialLoading(false);
                }
            }
        };
        getFingerprint();
        return () => { isMounted = false; };
    }, []); // Empty dependency array - run once

    // --- Auth State Effect ---
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
            console.log("Auth state changed:", currentUser?.uid || "No user");
            setUser(currentUser);
            if (currentUser && fingerprint) {
                // Run association asynchronously
                associateFingerprint({ fpId: fingerprint })
                    .then(() => console.log("Fingerprint associated with user"))
                    .catch(err => console.error("Failed to associate fingerprint:", err));
            }
            // Finish initial loading check if fingerprint is now known
            if (fingerprint !== null || error.includes("fingerprint")) {
                setIsInitialLoading(false);
            }
        });
        return () => unsubscribe();
    }, [fingerprint, error]); // Re-run if fingerprint loads or errors

    // --- Auth Handlers ---
    const handleLoginAttempt = useCallback(async (emailParam: string, passwordParam: string) => {
        setError(""); // Clear previous errors
        setIsOperationLoading(true);
        try {
            await signInWithEmailAndPassword(auth, emailParam, passwordParam);
            // Association happens in onAuthStateChanged effect
            setIsLoginModalOpen(false); // Close modal on success
        } catch (err: unknown) {
            const firebaseError = err as AuthError;
            console.error("Login error:", firebaseError);
            if (['auth/user-not-found', 'auth/wrong-password', 'auth/invalid-credential', 'auth/invalid-email'].includes(firebaseError.code)) {
                setError("Invalid email or password.");
            } else if (firebaseError.code === 'auth/too-many-requests') {
                setError("Too many login attempts. Please try again later.");
            } else {
                setError(`Login failed: ${firebaseError.message || 'Please try again.'}`);
            }
            throw err; // Re-throw so form's catch block can be notified if needed
        } finally {
            setIsOperationLoading(false);
        }
    }, [auth]); // Dependency: auth

    const handleSignupAttempt = useCallback(async (emailParam: string, passwordParam: string) => {
        setError("");
        setIsOperationLoading(true);

        if (!fingerprint) {
            const fpError = "Could not verify device fingerprint. Please refresh and try again.";
            setError(fpError);
            setIsOperationLoading(false);
            return;
        }

        try {
            // Check fingerprint first using Cloud Function
            console.log("Checking fingerprint before signup...");
            const fpCheckResult = await checkFingerprintExists({ fpId: fingerprint });
            const fpData = fpCheckResult.data as { exists: boolean; userId: string | null };

            if (fpData.exists && fpData.userId) {
                const fpExistsError = `This device seems linked to an existing account (User ID starting: ${fpData.userId.substring(0, 3)}...). Please log in or contact support.`;
                console.warn(`Signup blocked: Fingerprint ${fingerprint} linked to user ${fpData.userId}`);
                setError(fpExistsError);
                return; // Exit early
            }
            console.log("Fingerprint check passed.");

            // Proceed with signup
            const userCredential = await createUserWithEmailAndPassword(auth, emailParam, passwordParam);
            console.log("Signup successful:", userCredential.user.uid);

            // Associate fingerprint using Cloud Function after successful signup
            await associateFingerprint({ fpId: fingerprint });

            setIsSignupModalOpen(false); // Close modal on success

        } catch (err: unknown) {
            // Check if error was already set by fingerprint check
            if (!error) {
                const firebaseError = err as AuthError;
                console.error("Signup error:", firebaseError);
                if (firebaseError.code === 'auth/email-already-in-use') {
                    setError("This email is already registered. Please log in.");
                } else if (firebaseError.code === 'auth/weak-password') {
                    setError("Password is too weak (min. 6 characters).");
                } else if (firebaseError.code === 'auth/invalid-email') {
                    setError("Please enter a valid email address.");
                } else {
                    setError(`Signup failed: ${firebaseError.message || 'Please try again.'}`);
                }
            }
        } finally {
            setIsOperationLoading(false);
        }
    }, [auth, fingerprint, error, associateFingerprint, checkFingerprintExists]);

    const handleSocialAuthAttempt = useCallback(async (providerKey: string) => {
        setError("");
        setIsOperationLoading(true);

        if (!fingerprint) {
            setError("Could not verify device fingerprint. Please refresh and try again.");
            setIsOperationLoading(false);
            return; // Stop here
        }

        const socialProvider = providers[providerKey as keyof typeof providers];
        if (!socialProvider) {
            setError(`Invalid social provider: ${providerKey}`);
            setIsOperationLoading(false);
            return; // Stop here
        }

        try {
            // Check fingerprint first using Cloud Function
            console.log(`Checking fingerprint before ${providerKey} sign-in...`);
            const fpCheckResult = await checkFingerprintExists({ fpId: fingerprint });
            const fpData = fpCheckResult.data as { exists: boolean; userId: string | null };

            if (fpData.exists && fpData.userId) {
                const fpExistsError = `This device seems linked to an existing account (User ID starting: ${fpData.userId.substring(0, 6)}). Please log in or contact support.`;
                console.warn(`${providerKey} sign-in blocked: Fingerprint ${fingerprint} linked to user ${fpData.userId}`);
                setError(fpExistsError);
                throw new Error(fpExistsError);
            }
            console.log("Fingerprint check passed.");

            // Proceed with social sign in
            const userCredential = await signInWithPopup(auth, socialProvider);
            console.log(`${providerKey} sign-in successful:`, userCredential.user.uid);

            // Associate fingerprint using Cloud Function
            await associateFingerprint({ fpId: fingerprint });

            // Close modals on success
            setIsLoginModalOpen(false);
            setIsSignupModalOpen(false);

        } catch (err: unknown) {
            // Check if error was already set by fingerprint check
            if (!error) {
                const firebaseError = err as AuthError;
                console.error(`${providerKey} auth error:`, firebaseError);
                if (firebaseError.code === 'auth/account-exists-with-different-credential') {
                    setError("Account exists with this email but a different sign-in method.");
                } else if (['auth/popup-closed-by-user', 'auth/cancelled-popup-request'].includes(firebaseError.code)) {
                    setError("Sign-in popup was closed or cancelled.");
                } else {
                    setError(`Sign-in failed: ${firebaseError.message || 'Please try again.'}`);
                }
            }
        } finally {
            setIsOperationLoading(false);
        }
    }, [auth, fingerprint, error, associateFingerprint, checkFingerprintExists]);

    const handleLogout = useCallback(async () => {
        setError("");
        try {
            await signOut(auth);
            console.log("User signed out");
        } catch (err: unknown) {
            const firebaseError = err as AuthError;
            console.error("Error signing out:", firebaseError);
            setError("Failed to sign out. Please try again.");
        }
    }, [auth]);

    // --- Modal Control Functions ---
    const openLoginModal = useCallback(() => {
        setError(''); // Clear errors when opening
        setIsSignupModalOpen(false);
        setIsLoginModalOpen(true);
    }, []);

    const openSignupModal = useCallback(() => {
        setError(''); // Clear errors when opening
        setIsLoginModalOpen(false);
        setIsSignupModalOpen(true);
    }, []);

    const closeLoginModal = useCallback(() => setIsLoginModalOpen(false), []);
    const closeSignupModal = useCallback(() => setIsSignupModalOpen(false), []);

    const switchToSignup = useCallback(() => {
        closeLoginModal();
        openSignupModal(); // This already clears errors
    }, [closeLoginModal, openSignupModal]);

    const switchToLogin = useCallback(() => {
        closeSignupModal();
        openLoginModal(); // This already clears errors
    }, [closeSignupModal, openLoginModal]);


    // --- Render Logic ---
    if (isInitialLoading) { // Use the dedicated initial loading state
        return (
            <div className="flex justify-center items-center h-screen bg-zinc-900">
                <p className="text-white text-xl">Initializing...</p>
                {/* Optional Spinner */}
            </div>
        );
    }

    return (
        <header className="relative px-4 py-2">
            <nav className="bg-zinc-900 text-danger sticky top-0 shadow-md rounded-2xl py-3 z-40">
                <div className="container mx-auto px-4">
                    <div className="flex items-center justify-between">
                        {/* Logo/Brand and Desktop Navigation */}
                        <div className="flex items-center flex-shrink-0">
                            <a href="/" className="text-3xl lg:text-4xl font-orbital flex items-center font-bold px-2 py-2 text-[#00dd87]">
                                <img src="/leaf.png" alt="Gains Trackers Logo" className="mr-2 h-8 lg:h-10 w-auto"/>
                                Gains Trackers
                            </a>
                            <ul className="hidden lg:flex items-center ml-6">
                                <NavItem text={<a className={`${props.name.toLowerCase() === "nutrition" ? "text-info font-bold" : ""}`} href="/Nutrition">Nutrition</a>} />
                                <NavItem text={<a className={`${props.name.toLowerCase() === "groups" ? "text-info font-bold " : ""}`} href="/Groups">Workout Groups</a>} />
                                <NavItem text={<a className={`${props.name.toLowerCase() === "about-us" ? "text-info font-bold " : ""} `} href="/About-Us">About Us</a>} />
                            </ul>
                        </div>

                        {/* Authentication Buttons (Desktop) */}
                        <div className="hidden lg:flex items-center gap-3 flex-shrink-0">
                            {user ? (
                                <div className="flex items-center gap-3">
                                <span className="text-green-400 text-sm lg:text-base truncate max-w-[150px] lg:max-w-[250px]" title={user.email || user.displayName || 'User'}>
                                    Hello, {user.displayName || user.email?.split('@')[0] || "User"}
                                </span>
                                    <button
                                        className="border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white px-3 lg:px-4 py-1.5 lg:py-2 rounded-md transition-all text-sm lg:text-base"
                                        onClick={handleLogout}>
                                        Logout
                                    </button>
                                </div>
                            ) : (
                                <>
                                    <button
                                        className="border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-3 lg:px-4 py-1.5 lg:py-2 rounded-md transition-all text-sm lg:text-base"
                                        onClick={openLoginModal}> {/* Use callback */}
                                        Login
                                    </button>
                                    <button
                                        className="bg-green-500 text-white hover:bg-green-600 px-3 lg:px-4 py-1.5 lg:py-2 rounded-md transition-all text-sm lg:text-base"
                                        onClick={openSignupModal}> {/* Use callback */}
                                        Sign Up
                                    </button>
                                </>
                            )}
                        </div>

                        {/* Mobile menu button */}
                        <button
                            className="lg:hidden block text-gray-300 hover:text-white p-2"
                            type="button" onClick={() => setIsMenuOpen(!isMenuOpen)} aria-label="Toggle menu" aria-expanded={isMenuOpen}>
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                {isMenuOpen ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /> : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"/>}
                            </svg>
                        </button>
                    </div>

                    {/* Mobile Navigation Menu */}
                    <div className={`lg:hidden overflow-hidden transition-all duration-300 ease-in-out ${isMenuOpen ? "max-h-screen mt-4 opacity-100" : "max-h-0 mt-0 opacity-0"}`}>
                        <ul className="flex flex-col items-center border-t border-zinc-700 pt-4">
                            <NavItem text={<a className={`${props.name.toLowerCase() === "nutrition" ? "text-white font-bold underline" : "text-green-500"}`} href="/Nutrition">Nutrition</a>} />
                            <NavItem text={<a className={`${props.name.toLowerCase() === "groups" ? "text-white font-bold underline" : "text-green-500"}`} href="/Groups">Workout Groups</a>} />
                            <NavItem text={<a className={`${props.name.toLowerCase() === "about-us" ? "text-white font-bold underline" : "text-green-500"}`} href="/About-Us">About Us</a>}/>
                        </ul>
                        {/* Mobile Authentication Buttons */}
                        <div className="mt-4 pt-4 border-t border-zinc-700 flex flex-col items-center gap-3 px-4 pb-4">
                            {user ? (
                                <div className="flex flex-col items-center gap-3 w-full max-w-xs">
                                    <span className="text-green-400 text-center truncate w-full" title={user.email || user.displayName || 'User'}> Hello, {user.displayName || user.email?.split('@')[0] || "User"}</span>
                                    <button className="w-full border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white px-4 py-2 rounded-md transition-all" onClick={handleLogout}> Logout </button>
                                </div>
                            ) : (
                                <>
                                    <button className="w-full max-w-xs border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-4 py-2 rounded-md transition-all"
                                            onClick={() => { setIsMenuOpen(false); openLoginModal(); }}> {/* Close menu and open modal */}
                                        Login
                                    </button>
                                    <button className="w-full max-w-xs bg-green-500 text-white hover:bg-green-600 px-4 py-2 rounded-md transition-all"
                                            onClick={() => { setIsMenuOpen(false); openSignupModal(); }}> {/* Close menu and open modal */}
                                        Sign Up
                                    </button>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </nav>

            {/* --- Render Modals with Form Components --- */}
            <Modal
                isOpen={isLoginModalOpen}
                onClose={closeLoginModal}
                title="Login"
            >
                <LoginForm
                    onLoginSubmit={handleLoginAttempt}
                    onSocialAuth={handleSocialAuthAttempt}
                    onSwitchToSignup={switchToSignup}
                    isLoading={isOperationLoading}
                    // error={error} // Pass down the error state from Navbar
                />
            </Modal>

            <Modal
                isOpen={isSignupModalOpen}
                onClose={closeSignupModal}
                title="Create Account"
            >
                <SignupForm
                    onSignupSubmit={handleSignupAttempt}
                    onSocialAuth={handleSocialAuthAttempt}
                    onSwitchToLogin={switchToLogin}
                    isLoading={isOperationLoading}
                    error={error} // Pass down the error state from Navbar
                />
            </Modal>

        </header>
    );
}

export default Navbar;