import React, { useState } from "react";
import { motion } from "framer-motion";

export function DataDownload() {
  const [downloading, setDownloading] = useState(false);

  // Mock transactions
  const mockTransactions = [
    { date: "2025-09-01", description: "Salary Credit", amount: 50000 },
    { date: "2025-09-02", description: "ATM Withdrawal", amount: -2000 },
    { date: "2025-09-04", description: "UPI Payment", amount: -350 },
    { date: "2025-09-05", description: "Interest Credit", amount: 120 },
  ];

  // Helper: Convert to CSV string
  const toCSV = (data) => {
    const headers = Object.keys(data[0]).join(",");
    const rows = data.map((row) => Object.values(row).join(","));
    return [headers, ...rows].join("\n");
  };

  // Handle download
  const handleDownload = (format) => {
    setDownloading(true);
    setTimeout(() => {
      let blob;
      if (format === "csv") {
        const csv = toCSV(mockTransactions);
        blob = new Blob([csv], { type: "text/csv" });
      } else {
        const json = JSON.stringify(mockTransactions, null, 2);
        blob = new Blob([json], { type: "application/json" });
      }

      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `transactions.${format}`;
      link.click();
      setDownloading(false);
    }, 1000); // Simulate backend delay
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
          Export all your transactions for backup or analysis. Choose your
          preferred format below.
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
