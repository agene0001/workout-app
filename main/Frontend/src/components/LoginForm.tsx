// src/components/LoginForm.tsx (adjust path as needed)
"use client";
import React, { useState } from 'react';
// import { SocialLoginButtons } from './SocialLoginButtons'; // Assuming you extract SocialLoginButtons too

interface LoginFormProps {
    onLoginSubmit: (email: string, password: string) => Promise<void>;
    onSocialAuth: (provider: string) => Promise<void>;
    onSwitchToSignup: () => void;
    initialError?: string; // Optional: Pass initial error from Navbar if needed
    isLoading: boolean; // Get loading state from parent
}

export const LoginForm: React.FC<LoginFormProps> = ({
                                                        onLoginSubmit,
                                                        onSocialAuth,
                                                        onSwitchToSignup,
                                                        initialError = "",
                                                        isLoading,

                                                    }) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(initialError);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(""); // Clear local error before trying
        try {
            await onLoginSubmit(email, password);
            // No need to close modal here, parent will handle based on auth state change or success
        } catch (err: unknown) {
            // Parent handler should ideally manage error state for consistency,
            // but can set local error too if needed for immediate feedback.
            const errorMessage = err instanceof Error ? err.message : "Login failed";
            // You might want more specific error parsing here or let the parent handle it fully
            setError(errorMessage);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            {error && <p className="text-red-400 bg-red-900 bg-opacity-30 border border-red-600 px-3 py-2 rounded-md text-sm">{error}</p>}
            <div>
                <label className="block text-gray-300 mb-1 text-sm font-medium" htmlFor="login-email">Email</label>
                <input
                    id="login-email"
                    type="email"
                    className="w-full px-4 py-2 rounded bg-zinc-700 text-white border border-zinc-600 focus:border-green-500 focus:ring-1 focus:ring-green-500 focus:outline-none transition-colors"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    autoComplete="email"
                />
            </div>
            <div>
                <label className="block text-gray-300 mb-1 text-sm font-medium" htmlFor="login-password">Password</label>
                <input
                    id="login-password"
                    type="password"
                    className="w-full px-4 py-2 rounded bg-zinc-700 text-white border border-zinc-600 focus:border-green-500 focus:ring-1 focus:ring-green-500 focus:outline-none transition-colors"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete="current-password"
                />
            </div>
            <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-green-600 text-white py-2.5 rounded hover:bg-green-700 transition-all duration-200 disabled:opacity-70 disabled:cursor-wait font-semibold"
            >
                {isLoading ? "Logging in..." : "Login"}
            </button>
            <p className="text-gray-400 text-sm text-center pt-2">
                Don't have an account?{" "}
                <button
                    type="button"
                    className="text-green-500 hover:underline font-medium"
                    onClick={onSwitchToSignup} // Use prop
                >
                    Sign up
                </button>
            </p>
            {/* Pass the handlers down to SocialLoginButtons if extracted */}
            {/* <SocialLoginButtons onSocialAuth={onSocialAuth} isLoading={isLoading} /> */}
            {/* Or keep SocialLoginButtons logic here for simplicity */}
            <div className="flex flex-col space-y-3 mt-4">
                <div className="relative flex items-center">
                    <div className="flex-grow border-t border-gray-600"></div>
                    <span className="flex-shrink mx-4 text-gray-400 text-sm">or continue with</span>
                    <div className="flex-grow border-t border-gray-600"></div>
                </div>
                {/* ... Social Buttons calling onSocialAuth ... */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <button
                        type="button"
                        onClick={() => onSocialAuth('google')}
                        disabled={isLoading}
                        className="flex items-center justify-center bg-zinc-700 hover:bg-zinc-600 disabled:opacity-50 disabled:cursor-not-allowed text-white py-2 px-3 rounded transition-colors duration-200 w-full"
                    >
                        {/* Google SVG */} Google
                    </button>
                    <button
                        type="button"
                        onClick={() => onSocialAuth('github')}
                        disabled={isLoading}
                        className="flex items-center justify-center bg-gray-800 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed text-white py-2 px-3 rounded transition-colors duration-200 w-full"
                    >
                        {/* GitHub SVG */} GitHub
                    </button>
                </div>
            </div>
        </form>
    );
};