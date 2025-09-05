import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import axios from "axios";

export default function ResponsesPage() {
  const [responses, setResponses] = useState([]);
  const API_BASE = "http://127.0.0.1:5000/api";

  useEffect(() => {
    fetchResponses();
  }, []);

  const fetchResponses = async () => {
    try {
      const res = await axios.get(`${API_BASE}/responses`, {
        withCredentials: true,
      });
      setResponses(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Error fetching responses:", err);
      setResponses([]);
    }
  };

  const handleUndo = async (id) => {
    try {
      await axios.put(
        `${API_BASE}/responses/${id}/undo`,
        {},
        { withCredentials: true }
      );
      setResponses((prev) =>
        prev.map((item) =>
          item.id === id ? { ...item, status: "active" } : item
        )
      );
    } catch (err) {
      console.error("Error updating response:", err);
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-start bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black">
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
            {responses.map((item, index) => (
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
                  {item.user_name}
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
                <td className="px-4 py-2">
                  {item.status === "suspended" && (
                    <button
                      onClick={() => handleUndo(item.id)}
                      className="w-full px-3 py-1 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 transition"
                    >
                      Undo
                    </button>
                  )}
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
