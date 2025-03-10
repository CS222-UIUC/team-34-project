"use client";

import React, { useState } from "react";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import Link from "next/link";

const SignInClient: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      // Implement your login function here
      await login(email, password);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleGoogleLogin = async (credentialResponse: any) => {
    if (credentialResponse.credential) {
      const token = credentialResponse.credential;
      const payload = JSON.parse(atob(token.split(".")[1])); // Decode JWT payload

      try {
        // Implement your Google login function here
        await googleLogin(payload.email, payload.name);
      } catch (err: any) {
        setError(err.message);
      }
    }
  };

  return (
    <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
      <div className="flex justify-center items-center min-h-screen bg-gray-50">
        <div className="w-full max-w-md p-6 bg-white shadow-lg rounded-lg">
          <h1 className="text-3xl font-bold text-center mb-6">Sign In</h1>

          {error && <div className="text-red-500 text-center mb-4">{error}</div>}

          <form onSubmit={handleLogin} className="space-y-6">
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
              Login
            </button>
          </form>

          <div className="text-center mt-4">
            <Link href="/forgot-password" className="text-sm text-blue-600 hover:underline">
              Forgot your password?
            </Link>
          </div>

          <div className="my-6 flex items-center">
            <div className="flex-grow border-t border-gray-300"></div>
            <span className="mx-4 text-gray-500 text-sm">OR</span>
            <div className="flex-grow border-t border-gray-300"></div>
          </div>

          <div className="text-center">
            <GoogleLogin
              onSuccess={handleGoogleLogin}
              onError={() => setError("Google Sign-In failed. Please try again.")}
              theme="outline"
              size="large"
              text="continue_with"
            />
          </div>

          <div className="text-center mt-4">
            <p className="text-sm">
              Don’t have an account?{" "}
              <Link href="/sign-up" className="text-blue-600 hover:underline">
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
};

export default SignInClient;
