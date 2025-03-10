"use client";

import React, { useState } from "react";
import Link from "next/link";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";

const SignUpClient = () => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSignUp = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            await signup(name, email, password);
        } catch (err: any) {
            setError(err.message);
        }
    };

    return (
        <GoogleOAuthProvider clientId="462492634822-4b1hk554m81f29absrgt44mq9ijsnh8h.apps.googleusercontent.com">
            <div className="flex justify-center items-center min-h-screen bg-gray-50">
                <div className="w-full max-w-md p-6 bg-white shadow-lg rounded-lg">
                    <h1 className="text-3xl font-bold text-center mb-6">Sign Up</h1>

                    {error && <div className="text-red-500 text-center mb-4">{error}</div>}

                    <form onSubmit={handleSignUp} className="space-y-6">
                        <div>
                            <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                                Name
                            </label>
                            <input
                                type="text"
                                id="name"
                                className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                            />
                        </div>
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                                Email
                            </label>
                            <input
                                type="email"
                                id="email"
                                className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                                Password
                            </label>
                            <input
                                type="password"
                                id="password"
                                className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>
                        <button
                            type="submit"
                            className="w-full py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            Sign Up
                        </button>
                    </form>

                    <div className="text-center mt-4">
                        <p className="text-sm">
                            Already have an account?{" "}
                            <Link href="/sign-in" className="text-blue-600 hover:underline">
                                Sign in
                            </Link>
                        </p>
                    </div>

                    <div className="my-6 flex items-center">
                        <div className="flex-grow border-t border-gray-300"></div>
                        <span className="mx-4 text-gray-500 text-sm">OR</span>
                        <div className="flex-grow border-t border-gray-300"></div>
                    </div>

                    <div className="text-center">
                        <GoogleLogin
                            onSuccess={(credentialResponse) => console.log(credentialResponse)}
                            onError={() => setError("Google Sign-Up failed. Please try again.")}
                            theme="outline"
                            size="large"
                            text="continue_with"
                        />
                    </div>
                </div>
            </div>
        </GoogleOAuthProvider>
    );
};

export default SignUpClient;