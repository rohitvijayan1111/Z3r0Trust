import React, { useState } from "react";
import { motion } from "framer-motion";

export function MFAEnforcement() {
  const [step, setStep] = useState("challenge");
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");

  const handleChallenge = () => {
    setMessage("MFA code sent to your email/phone.");
    setStep("verify");
  };

  const handleVerify = () => {
    if (code === "123456") {
      setMessage("✅ MFA Verified! Access granted.");
    } else {
      setMessage("❌ Invalid MFA code.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md bg-white dark:bg-zinc-950 p-6 rounded-2xl shadow-lg"
      >
        <h2 className="text-xl font-bold mb-4 dark:text-white">
          MFA Enforcement
        </h2>

        {step === "challenge" && (
          <button
            onClick={handleChallenge}
            className="w-full rounded-lg bg-blue-600 text-white py-2 hover:bg-blue-700"
          >
            Request MFA Challenge →
          </button>
        )}

        {step === "verify" && (
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Enter MFA code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full rounded-lg border dark:border-neutral-700 bg-transparent px-4 py-2 dark:text-white"
            />
            <button
              onClick={handleVerify}
              className="w-full rounded-lg bg-green-600 text-white py-2 hover:bg-green-700"
            >
              Verify MFA →
            </button>
          </div>
        )}

        {message && (
          <p className="mt-4 text-center text-sm text-neutral-600 dark:text-neutral-300">
            {message}
          </p>
        )}
      </motion.div>
    </div>
  );
}
