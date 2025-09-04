import React, { useState } from "react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";
import { cn } from "../../lib/utils";
import { motion, AnimatePresence } from "framer-motion";

export function SignupFormDemo() {
  const [isSignup, setIsSignup] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(isSignup ? "Sign up submitted" : "Login submitted");
  };

  return (
    <div className="absolute inset-0 -z-10">
      <div className="absolute -top-20 -left-20 h-72 w-72 rounded-full bg-gradient-to-r from-purple-400 to-pink-500 opacity-30 blur-3xl" />
      <div className="absolute bottom-0 right-0 h-96 w-96 rounded-full bg-gradient-to-r from-cyan-400 to-blue-500 opacity-30 blur-3xl" />

      <div className="flex min-h-screen w-full items-center justify-center bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black px-4">
        {/* Lock Icon */}

        <div className="absolute top-6 left-6 z-50">
          <img src="lock.png" alt="lock" className="w-8 h-8" />
        </div>

        {/* Card Container */}
        <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-lg dark:bg-zinc-950 sm:p-10 overflow-hidden">
          <AnimatePresence mode="wait">
            {isSignup ? (
              <motion.div
                key="signup"
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -40 }}
                transition={{ duration: 0.6, ease: "easeInOut" }}
              >
                <h2 className="text-2xl font-bold text-neutral-800 dark:text-neutral-100 sm:text-3xl">
                  Create your account
                </h2>
                <p className="mt-2 text-sm text-neutral-600 dark:text-neutral-400 sm:text-base">
                  ZeroTrust secures and verifies your authentication process.
                </p>

                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                  <div className="grid gap-4 sm:grid-cols-2">
                    <LabelInputContainer>
                      <Label htmlFor="firstname">First name</Label>
                      <Input id="firstname" placeholder="Tyler" type="text" />
                    </LabelInputContainer>
                    <LabelInputContainer>
                      <Label htmlFor="lastname">Last name</Label>
                      <Input id="lastname" placeholder="Durden" type="text" />
                    </LabelInputContainer>
                  </div>

                  <LabelInputContainer>
                    <Label htmlFor="email">Email Address</Label>
                    <Input
                      id="email"
                      placeholder="projectmayhem@fc.com"
                      type="email"
                    />
                  </LabelInputContainer>

                  <LabelInputContainer>
                    <Label htmlFor="password">Password</Label>
                    <Input
                      id="password"
                      placeholder="••••••••"
                      type="password"
                    />
                  </LabelInputContainer>

                  <button
                    className="group relative w-full rounded-md bg-gradient-to-br from-black to-neutral-600 px-4 py-2.5 font-medium text-white shadow-md transition hover:opacity-90 dark:from-zinc-800 dark:to-zinc-700"
                    type="submit"
                  >
                    Sign up &rarr;
                    <BottomGradient />
                  </button>
                </form>

                <p className="mt-6 text-center text-sm text-neutral-600 dark:text-neutral-400">
                  Already have an account?{" "}
                  <button
                    type="button"
                    onClick={() => setIsSignup(false)}
                    className="font-medium text-indigo-600 hover:underline"
                  >
                    Log in
                  </button>
                </p>
              </motion.div>
            ) : (
              <motion.div
                key="login"
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -40 }}
                transition={{ duration: 0.6, ease: "easeInOut" }}
              >
                <h2 className="text-2xl font-bold text-neutral-800 dark:text-neutral-100 sm:text-3xl">
                  Welcome back
                </h2>
                <p className="mt-2 text-sm text-neutral-600 dark:text-neutral-400 sm:text-base">
                  Log in to continue to product with ZeroTrust securitylayer.
                </p>

                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                  <LabelInputContainer>
                    <Label htmlFor="email">Email Address</Label>
                    <Input
                      id="email"
                      placeholder="you@example.com"
                      type="email"
                    />
                  </LabelInputContainer>

                  <LabelInputContainer>
                    <Label htmlFor="password">Password</Label>
                    <Input
                      id="password"
                      placeholder="••••••••"
                      type="password"
                    />
                  </LabelInputContainer>

                  <button
                    className="group relative w-full rounded-md bg-gradient-to-br from-black to-neutral-600 px-4 py-2.5 font-medium text-white shadow-md transition hover:opacity-90 dark:from-zinc-800 dark:to-zinc-700"
                    type="submit"
                  >
                    Log in &rarr;
                    <BottomGradient />
                  </button>
                </form>

                <p className="mt-6 text-center text-sm text-neutral-600 dark:text-neutral-400">
                  Don’t have an account?{" "}
                  <button
                    type="button"
                    onClick={() => setIsSignup(true)}
                    className="font-medium text-indigo-600 hover:underline"
                  >
                    Sign up
                  </button>
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

/* Shared Components */
const BottomGradient = () => (
  <>
    <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover:opacity-100" />
    <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover:opacity-100" />
  </>
);

const LabelInputContainer = ({ children, className }) => (
  <div className={cn("flex w-full flex-col space-y-2", className)}>
    {children}
  </div>
);
