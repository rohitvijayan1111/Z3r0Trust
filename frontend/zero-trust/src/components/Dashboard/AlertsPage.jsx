import React, { useState } from "react";
import { motion } from "framer-motion";

const alertsDataInitial = [
  {
    id: 17,
    alert_name: "Suspicious Login",
    confidence_score: "medium",
    timestamp: "2025-09-04T08:00:00Z",
    user: "alice",
    email: "alice@example.com",
    ip: "203.0.113.45",
    location: "New York, USA",
    device: "Windows 10 / Chrome",
    action: "login_attempt",
    status: "suspended",
    failed_count: 5,
    blockedIP: false,
    blockedUser: false,
  },
  // You can add more alerts here
];

export function AlertsPage() {
  const [alertsData, setAlertsData] = useState(alertsDataInitial);

  const toggleBlockIP = (id) => {
    setAlertsData((prev) =>
      prev.map((alert) =>
        alert.id === id ? { ...alert, blockedIP: !alert.blockedIP } : alert
      )
    );
  };

  const toggleBlockUser = (id) => {
    setAlertsData((prev) =>
      prev.map((alert) =>
        alert.id === id ? { ...alert, blockedUser: !alert.blockedUser } : alert
      )
    );
  };

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-start bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black px-4 py-12">
      {/* Top-left Lock Icon */}
      <div className="absolute top-6 left-6 z-50">
        <img src="/lock.png" alt="lock" className="w-8 h-8" />
      </div>

      {/* Page Heading */}
      <h1 className="text-1xl sm:text-3xl font-extrabold dark:text-white text-black mb-6">
        Security Alerts
      </h1>

      {/* Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="w-full max-w-7xl overflow-x-auto"
      >
        <table className="min-w-full divide-y divide-gray-200 dark:divide-zinc-700 rounded-xl overflow-hidden">
          <thead className="bg-gray-200 dark:bg-zinc-800">
            <tr>
              {[
                "Alert Name",
                "Confidence Score",
                "Timestamp",
                "User",
                "Email",
                "IP",
                "Location",
                "Device",
                "Action",
                "Status",
                "Failed Count",
                "Block IP",
                "Block User",
              ].map((header) => (
                <th
                  key={header}
                  className="px-4 py-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-300"
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-zinc-900 divide-y divide-gray-200 dark:divide-zinc-700">
            {alertsData.map((alert, index) => (
              <motion.tr
                key={alert.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05, duration: 0.4 }}
                className="hover:bg-gray-50 dark:hover:bg-zinc-800 transition"
              >
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.alert_name}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.confidence_score}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {new Date(alert.timestamp).toLocaleString()}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.user}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.email}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.ip}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.location}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.device}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.action}
                </td>
                <td className="px-4 py-3 text-sm font-semibold">
                  <span
                    className={`px-2 py-1 rounded-full text-xs ${
                      alert.status === "suspended"
                        ? "bg-red-200 text-red-800 dark:bg-red-800 dark:text-red-200"
                        : "bg-green-200 text-green-800 dark:bg-green-800 dark:text-green-200"
                    }`}
                  >
                    {alert.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.failed_count}
                </td>
                {/* Block IP Button */}
                <td className="px-4 py-3">
                  <button
                    onClick={() => toggleBlockIP(alert.id)}
                    className={`w-full px-3 py-1 rounded-lg text-sm font-medium transition ${
                      alert.blockedIP
                        ? "bg-red-600 text-white hover:bg-red-700"
                        : "bg-green-600 text-white hover:bg-green-700"
                    }`}
                  >
                    {alert.blockedIP ? "Unblock IP" : "Block IP"}
                  </button>
                </td>
                {/* Block User Button */}
                <td className="px-4 py-3">
                  <button
                    onClick={() => toggleBlockUser(alert.id)}
                    className={`w-full px-3 py-1 rounded-lg text-sm font-medium transition ${
                      alert.blockedUser
                        ? "bg-red-600 text-white hover:bg-red-700"
                        : "bg-green-600 text-white hover:bg-green-700"
                    }`}
                  >
                    {alert.blockedUser ? "Unblock User" : "Block User"}
                  </button>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </motion.div>
    </div>
  );
}
