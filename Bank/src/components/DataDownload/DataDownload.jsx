import React, { useState } from "react";
import { motion } from "framer-motion";

export function DataDownload() {
  const [downloading, setDownloading] = useState(false);

  // --- Generate ~100k rows for ~5MB data ---
  const generateBigTransactions = () => {
    const transactions = [];
    for (let i = 1; i <= 100000; i++) {
      transactions.push({
        date: `2025-09-${String((i % 30) + 1).padStart(2, "0")}`,
        description: `Transaction #${i}`,
        amount: (Math.random() * 2000 - 1000).toFixed(2), // credit or debit
      });
    }
    return transactions;
  };

  // Static dataset (generated once)
  const bigTransactions = generateBigTransactions();

  // --- Helper: Convert to CSV string ---
  const toCSV = (data) => {
    const headers = Object.keys(data[0]).join(",");
    const rows = data.map((row) => Object.values(row).join(","));
    return [headers, ...rows].join("\n");
  };

  // --- Handle download ---
  const handleDownload = (format) => {
    setDownloading(true);
    setTimeout(() => {
      let blob;
      if (format === "csv") {
        const csv = toCSV(bigTransactions);
        blob = new Blob([csv], { type: "text/csv" });
      } else {
        const json = JSON.stringify(bigTransactions, null, 2);
        blob = new Blob([json], { type: "application/json" });
      }

      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `transactions.${format}`;
      link.click();

      setDownloading(false);
    }, 1000); // Simulated delay
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black p-6">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="rounded-2xl bg-white dark:bg-zinc-950 shadow-lg p-6 max-w-xl mx-auto"
      >
        <h2 className="text-xl font-bold text-neutral-800 dark:text-neutral-100 mb-4">
          Download Transaction History
        </h2>
        <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-6">
          Export a large dataset of transactions for testing big data downloads.
        </p>

        <div className="flex gap-4">
          <button
            onClick={() => handleDownload("csv")}
            disabled={downloading}
            className="rounded-lg bg-blue-500 px-4 py-2 text-white shadow-md hover:bg-blue-600 transition disabled:opacity-50"
          >
            {downloading ? "Preparing..." : "Download CSV"}
          </button>
          <button
            onClick={() => handleDownload("json")}
            disabled={downloading}
            className="rounded-lg bg-green-500 px-4 py-2 text-white shadow-md hover:bg-green-600 transition disabled:opacity-50"
          >
            {downloading ? "Preparing..." : "Download JSON"}
          </button>
        </div>
      </motion.div>
    </div>
  );
}
