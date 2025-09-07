import React, { useState } from "react";
import { motion } from "framer-motion";

export function InternalUserPanel() {
  const [customerInfo, setCustomerInfo] = useState(null);
  const [reports, setReports] = useState(null);

  const fetchCustomerInfo = () => {
    setCustomerInfo({
      name: "John Doe",
      account: "1234567890",
      balance: "₹52,300",
    });
  };

  const fetchReports = () => {
    setReports({
      suspiciousLogins: 4,
      failedTransfers: 2,
      unusualIPs: 3,
    });
  };

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-3xl mx-auto rounded-2xl bg-white dark:bg-zinc-950 shadow-lg p-6"
      >
        <h2 className="text-2xl font-bold mb-6 dark:text-white">
          Internal User Panel
        </h2>

        <div className="space-y-4">
          <button
            onClick={fetchCustomerInfo}
            className="w-full rounded-lg bg-blue-600 text-white px-4 py-2 hover:bg-blue-700"
          >
            Fetch Customer Info →
          </button>
          {customerInfo && (
            <div className="p-4 rounded-lg bg-gray-100 dark:bg-zinc-800 mt-2">
              <p>
                <b>Name:</b> {customerInfo.name}
              </p>
              <p>
                <b>Account:</b> {customerInfo.account}
              </p>
              <p>
                <b>Balance:</b> {customerInfo.balance}
              </p>
            </div>
          )}

          <button
            onClick={fetchReports}
            className="w-full rounded-lg bg-indigo-600 text-white px-4 py-2 hover:bg-indigo-700"
          >
            Fetch Reports →
          </button>
          {reports && (
            <div className="p-4 rounded-lg bg-gray-100 dark:bg-zinc-800 mt-2">
              <p>Suspicious Logins: {reports.suspiciousLogins}</p>
              <p>Failed Transfers: {reports.failedTransfers}</p>
              <p>Unusual IPs: {reports.unusualIPs}</p>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
}
