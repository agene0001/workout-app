"use client";
import React, {useState, useEffect} from "react";
import {NavItemProps} from "../types";
import {
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
    User,
    GoogleAuthProvider,
    // FacebookAuthProvider,
    GithubAuthProvider,
    // TwitterAuthProvider,
    // OAuthProvider,
    signInWithPopup
} from "firebase/auth";
import {auth} from "../firebase/config";

// Modal component - use React.memo to prevent unnecessary re-renders
const Modal = React.memo(({isOpen, onClose, title, children}: {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode
}) => {
    if (!isOpen) return null;

    return (<div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
        <div className="bg-zinc-800 p-6 rounded-lg w-full max-w-md" onClick={(e) => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-white">{title}</h2>
                <button
                    onClick={onClose}
                    className="text-gray-400 hover:text-white"
                >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                              d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>
            {children}
        </div>
    </div>);
});

// Ensure Modal has a display name for React DevTools
Modal.displayName = "Modal";

// Authentication providers configuration
const providers = {
    google: new GoogleAuthProvider(),
    // facebook: new FacebookAuthProvider(),
    github: new GithubAuthProvider(),
    // twitter: new TwitterAuthProvider(),
    // apple: new OAuthProvider('apple.com')
};

function Navbar(props: { name: string }) {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [user, setUser] = useState<User | null>(null);
    const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
    const [isSignupModalOpen, setIsSignupModalOpen] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [isAuthLoading, setIsAuthLoading] = useState(false);

    // Check authentication state when component mounts
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
            setUser(currentUser);
        });

        // Clean up subscription
        return () => unsubscribe();
    }, []);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setIsAuthLoading(true);
        try {
            await signInWithEmailAndPassword(auth, email, password);
            setIsLoginModalOpen(false);
            setEmail("");
            setPassword("");
        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : "An unknown error occurred";
            setError(errorMessage);
        } finally {
            setIsAuthLoading(false);
        }
    };

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setIsAuthLoading(true);
        try {
            await createUserWithEmailAndPassword(auth, email, password);
            setIsSignupModalOpen(false);
            setEmail("");
            setPassword("");
        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : "An unknown error occurred";
            setError(errorMessage);
        } finally {
            setIsAuthLoading(false);
        }
    };

    const handleSocialAuth = async (provider: string) => {
        setError("");
        setIsAuthLoading(true);
        try {
            await signInWithPopup(auth, providers[provider as keyof typeof providers]);
            setIsLoginModalOpen(false);
            setIsSignupModalOpen(false);
        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : "An unknown error occurred";
            setError(errorMessage);
        } finally {
            setIsAuthLoading(false);
        }
    };

    const handleLogout = async () => {
        try {
            await signOut(auth);
        } catch (err: unknown) {
            console.error("Error signing out:", err instanceof Error ? err.message : "Unknown error");
        }
    };

    const NavItem: React.FC<NavItemProps> = ({text}) => {
        const [isHovered, setIsHovered] = useState(false);

        return (<li
            className={`text-lg px-4 py-2 mx-1 cursor-pointer transition-all duration-200 ${isHovered ? "text-secondary scale-105" : "text-[#00dd87]"}`}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}>
            {text}
        </li>);
    };

    // Social login buttons component
    const SocialLoginButtons = () => {
        return (
            <div className="flex flex-col space-y-3 mt-4">
                <div className="relative flex items-center">
                    <div className="flex-grow border-t border-gray-600"></div>
                    <span className="flex-shrink mx-4 text-gray-400">or continue with</span>
                    <div className="flex-grow border-t border-gray-600"></div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                    <button
                        type="button"
                        onClick={() => handleSocialAuth('google')}
                        disabled={isAuthLoading}
                        className="flex items-center justify-center bg-zinc-700 hover:bg-zinc-600 text-white py-2 px-3 rounded transition-colors"
                    >
                        <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                            <path
                                fill="currentColor"
                                d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z"
                            />
                        </svg>
                        Google
                    </button>

                    <button
                        type="button"
                        onClick={() => handleSocialAuth('facebook')}
                        disabled={isAuthLoading}
                        className="flex items-center justify-center bg-blue-600 hover:bg-blue-700 text-white py-2 px-3 rounded transition-colors"
                    >
                        <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                            <path
                                fill="currentColor"
                                d="M22,12c0-5.52-4.48-10-10-10S2,6.48,2,12c0,4.84,3.44,8.87,8,9.8V15H8v-3h2V9.5C10,7.57,11.57,6,13.5,6H16v3h-2 c-0.55,0-1,0.45-1,1v2h3v3h-3v6.95C18.05,21.45,22,17.19,22,12z"
                            />
                        </svg>
                        Facebook
                    </button>
                </div>

                <div className="grid grid-cols-3 gap-3">
                    <button
                        type="button"
                        onClick={() => handleSocialAuth('github')}
                        disabled={isAuthLoading}
                        className="flex items-center justify-center bg-gray-800 hover:bg-gray-900 text-white py-2 px-3 rounded transition-colors"
                    >
                        <svg className="w-5 h-5 mr-1" viewBox="0 0 24 24">
                            <path
                                fill="currentColor"
                                d="M12,2C6.48,2,2,6.48,2,12c0,4.42,2.87,8.17,6.84,9.5c0.5,0.09,0.68-0.22,0.68-0.48c0-0.24-0.01-0.87-0.01-1.7c-2.78,0.6-3.37-1.34-3.37-1.34c-0.45-1.16-1.11-1.47-1.11-1.47c-0.91-0.62,0.07-0.6,0.07-0.6c1,0.07,1.53,1.03,1.53,1.03c0.89,1.52,2.34,1.08,2.91,0.83c0.09-0.65,0.35-1.09,0.63-1.34c-2.22-0.25-4.55-1.11-4.55-4.94c0-1.09,0.39-1.98,1.03-2.68c-0.1-0.25-0.45-1.27,0.1-2.64c0,0,0.84-0.27,2.75,1.02c0.8-0.22,1.65-0.33,2.5-0.33c0.85,0,1.7,0.11,2.5,0.33c1.91-1.29,2.75-1.02,2.75-1.02c0.55,1.37,0.2,2.39,0.1,2.64c0.64,0.7,1.03,1.59,1.03,2.68c0,3.84-2.34,4.68-4.57,4.93c0.36,0.31,0.68,0.92,0.68,1.85c0,1.34-0.01,2.41-0.01,2.74c0,0.27,0.18,0.58,0.69,0.48C19.14,20.16,22,16.42,22,12C22,6.48,17.52,2,12,2z"
                            />
                        </svg>
                        GitHub
                    </button>

                    <button
                        type="button"
                        onClick={() => handleSocialAuth('twitter')}
                        disabled={isAuthLoading}
                        className="flex items-center justify-center bg-blue-400 hover:bg-blue-500 text-white py-2 px-3 rounded transition-colors"
                    >
                        <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M22.46,6c-0.77,0.35-1.6,0.58-2.46,0.69c0.88-0.53,1.56-1.37,1.88-2.38c-0.83,0.5-1.75,0.85-2.72,1.05C18.37,4.5,17.26,4,16,4c-2.35,0-4.27,1.92-4.27,4.29c0,0.34,0.04,0.67,0.11,0.98C8.28,9.09,5.11,7.38,3,4.79c-0.37,0.63-0.58,1.37-0.58,2.15c0,1.49,0.75,2.81,1.91,3.56c-0.71,0-1.37-0.2-1.95-0.5v0.03c0,2.08,1.48,3.82,3.44,4.21c-0.36,0.1-0.74,0.15-1.13,0.15c-0.27,0-0.54-0.03-0.8-0.08c0.54,1.69,2.11,2.95,4,2.98c-1.46,1.16-3.31,1.84-5.33,1.84c-0.34,0-0.68-0.02-1.02-0.06C3.44,20.29,5.7,21,8.12,21c9.13,0,14.12-7.54,14.12-14.08c0-0.22-0.01-0.42-0.02-0.64C21.37,7.63,22,6.87,22,6"/>
                        </svg>
                        Twitter
                    </button>

                    <button
                        type="button"
                        onClick={() => handleSocialAuth('apple')}
                        disabled={isAuthLoading}
                        className="flex items-center justify-center bg-black hover:bg-gray-900 text-white py-2 px-3 rounded transition-colors"
                    >
                        <svg className="w-5 h-5 mr-1" viewBox="0 0 24 24">
                            <path
                                fill="currentColor"
                                d="M17.05,15.5c-.3.64-.68,1.23-1.13,1.75-.57.69-1.03,1.16-1.38,1.41-.55.41-1.14.62-1.77.63-.45,0-1-.13-1.63-.38s-1.21-.38-1.71-.38c-.55,0-1.13.13-1.76.38-.63.26-1.14.39-1.53.42-.59.02-1.18-.2-1.77-.67-.39-.29-.87-.78-1.45-1.49-.62-.76-1.13-1.63-1.52-2.61-.43-1.07-.65-2.11-.65-3.12,0-1.15.25-2.14.74-2.97.39-.65.9-1.17,1.54-1.55.64-.38,1.33-.58,2.08-.59.5,0,1.17.14,2,.42.83.28,1.36.42,1.58.42.17,0,.76-.16,1.77-.49.95-.3,1.75-.43,2.4-.38,1.77.15,3.1.89,3.98,2.23-1.58.96-2.37,2.3-2.36,4.03,0,1.34.5,2.46,1.49,3.34.44.42.94.74,1.49.97-.12.36-.25.7-.38,1.02zM13.29,2.71c0,1.05-.27,2.04-.82,2.97-.66,1.09-1.46,1.72-2.34,1.88-.11-.91-.17-1.77-.17-2.57,0-1.01.3-2.04.9-2.97.3-.47.68-.86,1.13-1.17.45-.31.87-.48,1.27-.52.12.91.19,1.71.19,2.38z"
                            />
                        </svg>
                        Apple
                    </button>
                </div>
            </div>
        );
    };

    return (<header className="relative px-4">
        <nav className="bg-zinc-900 text-danger sticky top-0 shadow-md rounded-2xl py-4">
            <div className="container mx-auto px-4">
                <div className="flex items-center justify-between">
                    {/* Logo/Brand and Desktop Navigation */}
                    <div className="flex items-center">

                        <a href="/" className="text-4xl font-orbital flex flex-row font-bold px-4 py-2">
                            <img src="/leaf.png" alt="favicon"
                                 className="pb-1 px-3 h-10 max-h-12 w-auto bg-zinc-900"/>
                            Gains Trackers
                        </a>

                        {/* Desktop Navigation Items */}
                        <ul className="hidden lg:flex items-center">
                            <NavItem
                                text={<a
                                    className={`${props.name.toLowerCase() === "nutrition" ? "text-info font-bold" : ""}`}
                                    href="/Nutrition">
                                    Nutrition
                                </a>}
                            />
                            <NavItem
                                text={<a
                                    className={`${props.name.toLowerCase() === "groups" ? "text-info font-bold " : ""}`}
                                    href="/Groups">
                                    Workout Groups
                                </a>}
                            />
                            <NavItem
                                text={<a
                                    className={`${props.name.toLowerCase() === "about-us" ? "text-info font-bold " : ""} `}
                                    href="/About-Us">
                                    About Us
                                </a>}
                            />
                        </ul>
                    </div>

                    {/* Authentication Buttons */}
                    <div className="hidden lg:flex items-center gap-3">
                        {user ? (<div className="flex items-center gap-3">
                            <span className="text-green-500">Hello, {user.email?.split('@')[0] || user.displayName || "User"}</span>
                            <button
                                className="border border-blue-400 text-blue-400 hover:bg-blue-400 hover:text-white px-4 py-2 rounded-md transition-all"
                                onClick={handleLogout}
                            >
                                Logout
                            </button>
                        </div>) : (<>
                            <button
                                className="border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-4 py-2 rounded-md transition-all"
                                onClick={() => setIsLoginModalOpen(true)}
                            >
                                Login
                            </button>
                            <button
                                className="bg-green-500 text-white hover:bg-green-600 px-4 py-2 rounded-md transition-all"
                                onClick={() => setIsSignupModalOpen(true)}
                            >
                                Sign Up
                            </button>
                        </>)}
                    </div>

                    {/* Mobile menu button */}
                    <button
                        className="lg:hidden block text-white"
                        type="button"
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                        aria-label="Toggle menu">
                        <svg
                            className="w-6 h-6"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24">
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="M4 6h16M4 12h16M4 18h16"
                            />
                        </svg>
                    </button>
                </div>

                {/* Mobile Navigation Menu */}
                <div
                    className={`${isMenuOpen ? "block" : "hidden"} lg:hidden mt-4`}
                >
                    {/* Mobile Nav Links */}
                    <ul className="flex flex-col items-center">
                        <NavItem
                            text={<a
                                className={`${props.name.toLowerCase() === "nutrition" ? "text-white font-bold underline" : "text-green-500"}`}
                                href="/Nutrition">
                                Nutrition
                            </a>}
                        />
                        <NavItem
                            text={<a
                                className={`${props.name.toLowerCase() === "groups" ? "text-white font-bold underline" : "text-green-500"}`}
                                href="/Groups">
                                Workout Groups
                            </a>}
                        />
                        <NavItem
                            text={<a
                                className={`${props.name.toLowerCase() === "about-us" ? "text-white font-bold underline" : "text-green-500"}`}
                                href="/About-Us">
                                About Us
                            </a>}
                        />
                    </ul>

                    {/* Mobile Authentication Buttons */}
                    <div className="mt-4 flex flex-col items-center gap-2">
                        {user ? (<div className="flex flex-col items-center gap-2 w-full max-w-md">
                            <span className="text-green-500">Hello, {user.email?.split('@')[0] || user.displayName || "User"}</span>
                            <button
                                className="w-full border border-red-500 text-red-500 hover:bg-red-500 hover:text-white px-4 py-2 rounded-md transition-all"
                                onClick={handleLogout}
                            >
                                Logout
                            </button>
                        </div>) : (<>
                            <button
                                className="w-full max-w-md border border-green-500 text-green-500 hover:bg-green-500 hover:text-white px-4 py-2 rounded-md transition-all"
                                onClick={() => setIsLoginModalOpen(true)}
                            >
                                Login
                            </button>
                            <button
                                className="w-full max-w-md bg-green-500 text-white hover:bg-green-600 px-4 py-2 rounded-md transition-all"
                                onClick={() => setIsSignupModalOpen(true)}
                            >
                                Sign Up
                            </button>
                        </>)}
                    </div>
                </div>
            </div>
        </nav>

        {/* Login Modal */}
        <Modal
            isOpen={isLoginModalOpen}
            onClose={() => setIsLoginModalOpen(false)}
            title="Login"
        >
            <form onSubmit={handleLogin} className="space-y-4">
                {error && <p className="text-red-500 text-sm">{error}</p>}
                <div>
                    <label className="block text-gray-300 mb-1" htmlFor="email">Email</label>
                    <input
                        id="email"
                        type="email"
                        className="w-full px-4 py-2 rounded bg-zinc-700 text-white border border-zinc-600 focus:border-green-500 focus:outline-none"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label className="block text-gray-300 mb-1" htmlFor="password">Password</label>
                    <input
                        id="password"
                        type="password"
                        className="w-full px-4 py-2 rounded bg-zinc-700 text-white border border-zinc-600 focus:border-green-500 focus:outline-none"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button
                    type="submit"
                    disabled={isAuthLoading}
                    className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600 transition-all disabled:bg-green-800 disabled:cursor-not-allowed"
                >
                    {isAuthLoading ? "Logging in..." : "Login"}
                </button>
                <p className="text-gray-400 text-sm text-center">
                    Don't have an account?{" "}
                    <button
                        type="button"
                        className="text-green-500 hover:underline"
                        onClick={() => {
                            setIsLoginModalOpen(false);
                            setIsSignupModalOpen(true);
                        }}>
                        Sign up
                    </button>
                </p>

                <SocialLoginButtons />
            </form>
        </Modal>

        {/* Signup Modal */}
        <Modal
            isOpen={isSignupModalOpen}
            onClose={() => setIsSignupModalOpen(false)}
            title="Sign Up"
        >
            <form onSubmit={handleSignup} className="space-y-4">
                {error && <p className="text-red-500 text-sm">{error}</p>}
                <div>
                    <label className="block text-gray-300 mb-1" htmlFor="signup-email">Email</label>
                    <input
                        id="signup-email"
                        type="email"
                        className="w-full px-4 py-2 rounded bg-zinc-700 text-white border border-zinc-600 focus:border-green-500 focus:outline-none"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label className="block text-gray-300 mb-1" htmlFor="signup-password">Password</label>
                    <input
                        id="signup-password"
                        type="password"
                        className="w-full px-4 py-2 rounded bg-zinc-700 text-white border border-zinc-600 focus:border-green-500 focus:outline-none"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button
                    type="submit"
                    disabled={isAuthLoading}
                    className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600 transition-all disabled:bg-green-800 disabled:cursor-not-allowed"
                >
                    {isAuthLoading ? "Creating Account..." : "Create Account"}
                </button>
                <p className="text-gray-400 text-sm text-center">
                    Already have an account?{" "}
                    <button
                        type="button"
                        className="text-green-500 hover:underline"
                        onClick={() => {
                            setIsSignupModalOpen(false);
                            setIsLoginModalOpen(true);
                        }}
                    >
                        Login
                    </button>
                </p>

                <SocialLoginButtons />
            </form>
        </Modal>
    </header>);
}

export default Navbar;