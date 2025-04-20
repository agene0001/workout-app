// src/components/SignupForm.tsx
"use client";
import React, { useState } from 'react';

// Define the props the SignupForm will accept
interface SignupFormProps {
    onSignupSubmit: (email: string, password: string) => Promise<void>;
    onSocialAuth: (provider: string) => Promise<void>;
    onSwitchToLogin: () => void;
    error: string; // Display error passed from parent
    isLoading: boolean; // Get loading state from parent
}

export const SignupForm: React.FC<SignupFormProps> = ({
                                                          onSignupSubmit,
                                                          onSocialAuth,
                                                          onSwitchToLogin,
                                                          error, // Use the error prop from Navbar
                                                          isLoading,
                                                      }) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    // Removed local error state

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        // Don't clear parent error here
        try {
            if(password !== confirmPassword) throw new Error(
                "Passwords do not match"
            )
            await onSignupSubmit(email, password);
            // Parent handles success
        } catch (err) {
            // Error is already set in the parent by onSignupSubmit throwing/setting state
            console.log("Signup form caught error:", err);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            {/* Display the error passed down from Navbar */}
            {error && <p className="text-red-400 bg-red-900 bg-opacity-30 border border-red-600 px-3 py-2 rounded-md text-sm">{error}</p>}
            <div>
                <label className="block text-gray-300 mb-1 text-sm font-medium" htmlFor="signup-email">Email</label>
                <input
                    id="signup-email"
                    type="email"
                    className="w-full px-4 py-2 rounded bg-zinc-700 text-white border border-zinc-600 focus:border-green-500 focus:ring-1 focus:ring-green-500 focus:outline-none transition-colors"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    autoComplete="email"
                />
            </div>
            <div>
                <label className="block text-gray-300 mb-1 text-sm font-medium" htmlFor="signup-password">Password (min. 6 characters)</label>
                <input
                    id="signup-password"
                    type="password"
                    className="w-full px-4 py-2 rounded bg-zinc-700 text-white border border-zinc-600 focus:border-green-500 focus:ring-1 focus:ring-green-500 focus:outline-none transition-colors"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete="new-password"
                />
            </div>
            <div>
                <label className="block text-gray-300 mb-1 text-sm font-medium" htmlFor="signup-password-confirm">Confirm Password (min. 6 characters)</label>
                <input
                    id="signup-password-confirm"
                    type="password"
                    className="w-full px-4 py-2 rounded bg-zinc-700 text-white border border-zinc-600 focus:border-green-500 focus:ring-1 focus:ring-green-500 focus:outline-none transition-colors"
                    value={password}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    autoComplete="new-password"
                />
            </div>
            <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-green-600 text-white py-2.5 rounded hover:bg-green-700 transition-all duration-200 disabled:opacity-70 disabled:cursor-wait font-semibold"
            >
                {isLoading ? "Creating Account..." : "Create Account"}
            </button>
            <p className="text-gray-400 text-sm text-center pt-2">
                Already have an account?{" "}
                <button
                    type="button"
                    className="text-green-500 hover:underline font-medium"
                    onClick={onSwitchToLogin} // Use prop
                >
                    Login
                </button>
            </p>
            {/* --- Social Login Buttons --- */}
            <div className="flex flex-col space-y-3 mt-4">
                <div className="relative flex items-center">
                    <div className="flex-grow border-t border-gray-600"></div>
                    <span className="flex-shrink mx-4 text-gray-400 text-sm">or continue with</span>
                    <div className="flex-grow border-t border-gray-600"></div>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <button
                        type="button"
                        onClick={() => onSocialAuth('google')} // Use prop
                        disabled={isLoading}
                        className="flex items-center justify-center bg-zinc-700 hover:bg-zinc-600 disabled:opacity-50 disabled:cursor-not-allowed text-white py-2 px-3 rounded transition-colors duration-200 w-full"
                    >
                        <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24"> {/* Google SVG */}
                            <path fill="currentColor" d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z" />
                        </svg>
                        Google
                    </button>
                    <button
                        type="button"
                        onClick={() => onSocialAuth('github')} // Use prop
                        disabled={isLoading}
                        className="flex items-center justify-center bg-gray-800 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed text-white py-2 px-3 rounded transition-colors duration-200 w-full"
                    >
                        <svg className="w-5 h-5 mr-1" viewBox="0 0 24 24"> {/* GitHub SVG */}
                            <path fill="currentColor" d="M12,2C6.48,2,2,6.48,2,12c0,4.42,2.87,8.17,6.84,9.5c0.5,0.09,0.68-0.22,0.68-0.48c0-0.24-0.01-0.87-0.01-1.7c-2.78,0.6-3.37-1.34-3.37-1.34c-0.45-1.16-1.11-1.47-1.11-1.47c-0.91-0.62,0.07-0.6,0.07-0.6c1,0.07,1.53,1.03,1.53,1.03c0.89,1.52,2.34,1.08,2.91,0.83c0.09-0.65,0.35-1.09,0.63-1.34c-2.22-0.25-4.55-1.11-4.55-4.94c0-1.09,0.39-1.98,1.03-2.68c-0.1-0.25-0.45-1.27,0.1-2.64c0,0,0.84-0.27,2.75,1.02c0.8-0.22,1.65-0.33,2.5-0.33c0.85,0,1.7,0.11,2.5,0.33c1.91-1.29,2.75-1.02,2.75-1.02c0.55,1.37,0.2,2.39,0.1,2.64c0.64,0.7,1.03,1.59,1.03,2.68c0,3.84-2.34,4.68-4.57,4.93c0.36,0.31,0.68,0.92,0.68,1.85c0,1.34-0.01,2.41-0.01,2.74c0,0.27,0.18,0.58,0.69,0.48C19.14,20.16,22,16.42,22,12C22,6.48,17.52,2,12,2z" />
                        </svg>
                        GitHub
                    </button>
                </div>
            </div>
        </form>
    );
};