import React from "react";
import { motion } from "framer-motion";

// Sample response data
const responseData = [
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
  },
  // Add more response objects here
];

export default function ResponsesPage() {
  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-start bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black px-4 py-12">
      <div className="absolute top-6 left-6 z-50">
        <img src="/lock.png" alt="lock" className="w-8 h-8" />
      </div>

      <h1 className="text-2xl sm:text-3xl font-bold dark:text-white text-black mb-6">
        Responses
      </h1>

      <div className="w-full rounded-xl shadow-lg bg-white/5 dark:bg-zinc-900/50 backdrop-blur-md p-4">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-100 dark:bg-zinc-800/50">
            <tr>
              {[
                "Alert Name",
                "Confidence",
                "Timestamp",
                "User",
                "Email",
                "IP",
                "Location",
                "Device",
                "Action",
                "Status",
                "Failed Count",
                "Undo",
              ].map((header) => (
                <th
                  key={header}
                  className="px-4 py-2 text-left text-sm font-medium text-gray-700 dark:text-gray-300"
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {responseData.map((item, index) => (
              <motion.tr
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05, duration: 0.3 }}
                className="hover:bg-gray-100/20 dark:hover:bg-white/10 transition-colors"
              >
                <td className="px-4 py-2 text-sm dark:text-white">
                  {item.alert_name}
                </td>
                <td className="px-4 py-2 text-sm dark:text-white">
                  {item.confidence_score}
                </td>
                <td className="px-4 py-2 text-sm dark:text-white">
                  {new Date(item.timestamp).toLocaleString()}
                </td>
                <td className="px-4 py-2 text-sm dark:text-white">
                  {item.user}
                </td>
                <td className="px-4 py-2 text-sm dark:text-white">
                  {item.email}
                </td>
                <td className="px-4 py-2 text-sm dark:text-white">{item.ip}</td>
                <td className="px-4 py-2 text-sm dark:text-white">
                  {item.location}
                </td>
                <td className="px-4 py-2 text-sm dark:text-white">
                  {item.device}
                </td>
                <td className="px-4 py-2 text-sm dark:text-white">
                  {item.action}
                </td>
                <td className="px-4 py-3 text-sm font-semibold">
                  <span
                    className={`px-2 py-1 rounded-full text-xs ${
                      item.status === "suspended"
                        ? "bg-red-200 text-red-800 dark:bg-red-800 dark:text-red-200"
                        : "bg-green-200 text-green-800 dark:bg-green-800 dark:text-green-200"
                    }`}
                  >
                    {item.status}
                  </span>
                </td>
                <td className="px-4 py-2 text-sm dark:text-white">
                  {item.failed_count}
                </td>
                {/* Static Undo Button */}
                <td className="px-4 py-2">
                  <button className="w-full px-3 py-1 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 transition">
                    Undo
                  </button>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
