import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

export function UserDashboard() {
  const [balance, setBalance] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const session_jwt = localStorage.getItem("session_jwt");

  useEffect(() => {
    // 🟢 Simulate fetching from backend
    setTimeout(() => {
      if (!session_jwt) {
        setError("No session found. Please log in.");
        setLoading(false);
        return;
      }

      // Mock data
      setBalance(152430.75);
      setTransactions([
        { description: "Salary Credit", amount: 50000, date: "2025-09-01" },
        { description: "Electricity Bill", amount: -3200, date: "2025-08-28" },
        { description: "UPI Payment", amount: -1500, date: "2025-08-25" },
        { description: "Stock Dividend", amount: 2500, date: "2025-08-20" },
      ]);
      setLoading(false);
    }, 1000); // fake API delay
  }, [session_jwt]);

  const handleLogout = () => {
    localStorage.removeItem("session_jwt");
    window.location.reload(); // Reload app → goes back to login
  };

  if (loading) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black">
        <p className="text-lg text-neutral-600 dark:text-neutral-300 animate-pulse">
          Loading dashboard...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black p-6">
      {/* Header */}
      <header className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-neutral-800 dark:text-neutral-100">
          Bank Dashboard
        </h1>
        <button
          onClick={handleLogout}
          className="rounded-lg bg-red-500 px-4 py-2 text-white shadow-md hover:bg-red-600 transition"
        >
          Logout
        </button>
      </header>

      {/* Balance Card */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mb-8 rounded-2xl bg-white dark:bg-zinc-950 shadow-lg p-6"
      >
        <h2 className="text-lg font-semibold text-neutral-700 dark:text-neutral-200">
          Account Balance
        </h2>
        <p className="mt-2 text-3xl font-bold text-green-600">
          ₹ {balance?.toLocaleString() || "0.00"}
        </p>
      </motion.div>

      {/* Transactions Card */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        className="rounded-2xl bg-white dark:bg-zinc-950 shadow-lg p-6"
      >
        <h2 className="text-lg font-semibold text-neutral-700 dark:text-neutral-200 mb-4">
          Recent Transactions
        </h2>
        <div className="space-y-3">
          {transactions.length > 0 ? (
            transactions.map((tx, idx) => (
              <div
                key={idx}
                className="flex justify-between items-center rounded-lg border border-neutral-200 dark:border-neutral-800 p-3"
              >
                <div>
                  <p className="text-sm font-medium text-neutral-800 dark:text-neutral-100">
                    {tx.description}
                  </p>
                  <p className="text-xs text-neutral-500 dark:text-neutral-400">
                    {tx.date}
                  </p>
                </div>
                <p
                  className={`font-semibold ${
                    tx.amount < 0 ? "text-red-500" : "text-green-500"
                  }`}
                >
                  {tx.amount < 0 ? "-" : "+"}₹{Math.abs(tx.amount)}
                </p>
              </div>
            ))
          ) : (
            <p className="text-sm text-neutral-500">No recent transactions.</p>
          )}
        </div>
      </motion.div>
    </div>
  );
}
