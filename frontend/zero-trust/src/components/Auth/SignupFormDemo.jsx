import React, { useState } from "react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";
import { cn } from "../../lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { signupUser, loginUser } from "../../lib/api";
import { useNavigate } from "react-router-dom";




export function SignupFormDemo() {
    const [isSignup, setIsSignup] = useState(true);
    const [formData, setFormData] = useState({});
    const [message, setMessage] = useState("");
    
    const navigate = useNavigate();
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

   const handleSubmit = async (e) => {
     e.preventDefault();
     setMessage("");

     try {
       if (isSignup) {
         const res = await signupUser(formData);
         setMessage(res.message || "Signup successful!");
         if (res.message === "User created successfully") {
           navigate("/dashboard"); // redirect after signup
         }
       } else {
         const res = await loginUser(formData);
         if (res.token) {
           localStorage.setItem("token", res.token);
           setMessage("Login successful!");
           navigate("/dashboard"); // redirect after login
         } else {
           setMessage(res.message || "Login failed");
         }
       }
     } catch (err) {
       setMessage("Something went wrong!");
       console.error(err);
     }
   };


  return (
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

                {message && (
                  <p className="mt-2 text-sm text-green-500">{message}</p>
                )}

                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                  <div className="grid gap-4 sm:grid-cols-2">
                    <LabelInputContainer>
                      <Label htmlFor="first_name">First name</Label>
                      <Input
                        id="first_name"
                        type="text"
                        onChange={handleChange}
                      />
                    </LabelInputContainer>
                    <LabelInputContainer>
                      <Label htmlFor="last_name">Last name</Label>
                      <Input
                        id="last_name"
                        type="text"
                        onChange={handleChange}
                      />
                    </LabelInputContainer>
                  </div>

                  <LabelInputContainer>
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" onChange={handleChange} />
                  </LabelInputContainer>

                  <LabelInputContainer>
                    <Label htmlFor="password">Password</Label>
                    <Input
                      id="password"
                      type="password"
                      onChange={handleChange}
                    />
                  </LabelInputContainer>

                  <button className="group relative w-full rounded-md bg-gradient-to-br from-black to-neutral-600 px-4 py-2.5 font-medium text-white shadow-md transition hover:opacity-90 dark:from-zinc-800 dark:to-zinc-700">
                    Sign up &rarr;
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
                  Log in to continue with ZeroTrust security layer.
                </p>

                {message && (
                  <p className="mt-2 text-sm text-red-500">{message}</p>
                )}

                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                  <LabelInputContainer>
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" onChange={handleChange} />
                  </LabelInputContainer>

                  <LabelInputContainer>
                    <Label htmlFor="password">Password</Label>
                    <Input
                      id="password"
                      type="password"
                      onChange={handleChange}
                    />
                  </LabelInputContainer>

                  <button className="group relative w-full rounded-md bg-gradient-to-br from-black to-neutral-600 px-4 py-2.5 font-medium text-white shadow-md transition hover:opacity-90 dark:from-zinc-800 dark:to-zinc-700">
                    Log in &rarr;
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

const LabelInputContainer = ({ children, className }) => (
  <div className={cn("flex w-full flex-col space-y-2", className)}>
    {children}
  </div>
);
