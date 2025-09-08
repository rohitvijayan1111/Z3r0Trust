import React, { useState } from "react";
import { motion } from "framer-motion";
const proxyUrl = import.meta.env.VITE_PROXY_URL;

export function FundTransfer() {
  const [toAccount, setToAccount] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");

  const session_jwt = localStorage.getItem("session_jwt");
  const authResponse = JSON.parse(localStorage.getItem("auth_response"));
  const userEmail = authResponse?.user_id; // X-User-Email header

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!toAccount || !amount || isNaN(amount) || amount <= 0) {
      setMessage("❌ Please enter a valid account and amount.");
      return;
    }

    if (!session_jwt || !userEmail) {
      setMessage("❌ You are not logged in.");
      return;
    }

    try {
      const response = await fetch(`${proxyUrl}/api/transfer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session_jwt}`,
          "X-User-Email": userEmail,
        },
        body: JSON.stringify({
          from_account_number: "111722293", // 👈 ideally get from authResponse
          to_account_number: toAccount,
          amount: parseFloat(amount),
        }),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage("✅ " + result.message);
      } else {
        setMessage("❌ " + (result.detail || result.message || "Transfer failed"));
      }
    } catch (err) {
      console.error(err);
      setMessage("❌ Backend unavailable.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black flex items-center justify-center p-6">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeInOut" }}
        className="w-full max-w-lg rounded-2xl bg-white dark:bg-zinc-950 shadow-lg p-6 sm:p-10"
      >
        <h2 className="text-2xl font-bold text-neutral-800 dark:text-neutral-100 mb-6">
          Fund Transfer
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Account Number */}
          <div>
            <label
              htmlFor="toAccount"
              className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2"
            >
              To Account
            </label>
            <input
              id="toAccount"
              type="text"
              placeholder="Enter account number"
              value={toAccount}
              onChange={(e) => setToAccount(e.target.value)}
              className="w-full rounded-lg border border-neutral-300 dark:border-neutral-700 bg-transparent px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none dark:text-white"
            />
          </div>

          {/* Amount */}
          <div>
            <label
              htmlFor="amount"
              className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2"
            >
              Amount (₹)
            </label>
            <input
              id="amount"
              type="number"
              placeholder="Enter amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="w-full rounded-lg border border-neutral-300 dark:border-neutral-700 bg-transparent px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none dark:text-white"
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            className="w-full rounded-lg bg-gradient-to-br from-indigo-600 to-purple-600 px-4 py-2.5 text-white font-medium shadow-md hover:opacity-90 transition"
          >
            Transfer Money →
          </button>
        </form>

        {/* Message */}
        {message && (
          <p className="mt-6 text-center text-sm font-medium text-green-600 dark:text-green-400">
            {message}
          </p>
        )}
      </motion.div>
    </div>
  );
}
