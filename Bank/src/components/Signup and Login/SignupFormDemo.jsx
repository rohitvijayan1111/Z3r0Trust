import React, { useState } from "react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";
import { cn } from "../../lib/utils";
import { motion } from "framer-motion";

const proxyUrl = import.meta.env.VITE_PROXY_URL;

export function SignupFormDemo1() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Login submitted");

    try {
      const response = await fetch(`${proxyUrl}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, request_type: "web" }),
      });

      const result = await response.json();
      console.log("Backend response:", result);

      // ✅ Store the full response in localStorage
      localStorage.setItem("auth_response", JSON.stringify(result));

      if (result.status === "success" && result.session_jwt) {
        // ✅ Store important fields separately
        localStorage.setItem("session_jwt", result.session_jwt);
        localStorage.setItem("user_id", result.attributes.user_id);

        setMessage("✅ Login successful!");
        alert("✅ Login successful!"); // 🔔 Show alert
        window.location.href = "/dashboard";
      } else {
        setMessage("❌ " + (result.message || "Login failed"));
      }
    } catch (err) {
      console.error("Error calling backend:", err);
      setMessage("❌ Backend unavailable.");
    }
  };

  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black px-4">
      <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-lg dark:bg-zinc-950 sm:p-10 overflow-hidden">
        <motion.div
          key="login"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeInOut" }}
        >
          <h2 className="text-2xl font-bold text-neutral-800 dark:text-neutral-100 sm:text-3xl">
            Welcome back
          </h2>
          <p className="mt-2 text-sm text-neutral-600 dark:text-neutral-400 sm:text-base">
            Log in to continue with Bank Management App.
          </p>

          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <LabelInputContainer>
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                placeholder="you@example.com"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </LabelInputContainer>

            <LabelInputContainer>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                placeholder="••••••••"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
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

          {message && (
            <p className="mt-4 text-center text-sm text-red-500">{message}</p>
          )}
        </motion.div>
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
