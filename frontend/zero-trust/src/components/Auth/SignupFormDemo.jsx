import React, { useState } from "react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";
import { cn } from "../../lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { AuthProvider, Descope } from "@descope/react-sdk";
import { useNavigate } from "react-router-dom";

export function SignupFormDemo() {
  const [isSignup, setIsSignup] = useState(true);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  return (
    <AuthProvider projectId="P32Dj1SFaOxhwz4v0i9D6jseEJny">
      <div className="absolute inset-0 -z-10">
        {/* Background Blurs */}
        <div className="absolute -top-20 -left-20 h-72 w-72 rounded-full bg-gradient-to-r from-purple-400 to-pink-500 opacity-30 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-96 w-96 rounded-full bg-gradient-to-r from-cyan-400 to-blue-500 opacity-30 blur-3xl" />

        <div className="flex min-h-screen w-full items-center justify-center bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black px-4">
          <div className="absolute top-6 left-6 z-50">
            <img src="lock.png" alt="lock" className="w-8 h-8" />
          </div>

          <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-lg dark:bg-zinc-950 sm:p-10 overflow-hidden">
            <AnimatePresence mode="wait">
              <motion.div
                key={isSignup ? "signup" : "login"}
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -40 }}
                transition={{ duration: 0.6, ease: "easeInOut" }}
              >
                <h2 className="text-2xl font-bold text-neutral-800 dark:text-neutral-100 sm:text-3xl">
                  {isSignup ? "Create your account" : "Welcome back"}
                </h2>
                <p className="mt-2 text-sm text-neutral-600 dark:text-neutral-400 sm:text-base">
                  {isSignup
                    ? "ZeroTrust secures and verifies your authentication process."
                    : "Log in to continue with ZeroTrust security layer."}
                </p>

                {message && (
                  <p
                    className={`mt-2 text-sm ${
                      isSignup ? "text-green-500" : "text-red-500"
                    }`}
                  >
                    {message}
                  </p>
                )}

                {/* Descope Auth Form */}
                <div className="mt-8">
                  <Descope
                    flowId={
                      isSignup
                        ? "passwords-with-explicit-sign-up"
                        : "login-with-password"
                    }
                    theme="light"
                    onSuccess={(e) => {
                      // Store session token & user info in localStorage
                      localStorage.setItem(
                        "descopeToken",
                        e.detail.user.sessionToken
                      );
                      localStorage.setItem(
                        "descopeUser",
                        JSON.stringify(e.detail.user)
                      );

                      const role =
                        localStorage.getItem("userRole") || "customer"; // fallback to "customer"
                      setMessage(
                        isSignup ? "Signup successful!" : "Login successful!"
                      );

                      // Navigate based on role
                      if (role === "soc") {
                        navigate("/dashboard");
                      } else {
                        navigate("/integrateApi");
                      } // Redirect to dashboard
                    }}
                    onError={(err) => {
                      console.error("Auth Error:", err);
                      setMessage("Authentication failed. Try again.");
                    }}
                  />
                </div>

                <p className="mt-6 text-center text-sm text-neutral-600 dark:text-neutral-400">
                  {isSignup
                    ? "Already have an account? "
                    : "Don’t have an account? "}
                  <button
                    type="button"
                    onClick={() => {
                      setIsSignup(!isSignup);
                      setMessage("");
                    }}
                    className="font-medium text-indigo-600 hover:underline"
                  >
                    {isSignup ? "Log in" : "Sign up"}
                  </button>
                </p>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </AuthProvider>
  );
}

// Helper for label-input spacing
const LabelInputContainer = ({ children, className }) => (
  <div className={cn("flex w-full flex-col space-y-2", className)}>
    {children}
  </div>
);
