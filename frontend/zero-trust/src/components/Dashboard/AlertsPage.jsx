import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import axios from "axios";

export function AlertsPage() {
  const [alertsData, setAlertsData] = useState([]);
  const API_BASE = "http://127.0.0.1:5000/api";

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const res = await axios.get(`${API_BASE}/alerts`);
      setAlertsData(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Error fetching alerts:", err);
      setAlertsData([]);
    }
  };

  const handleToggleBlockIP = async (alert) => {
    try {
      if (alert.blockedIP) {
        // Call undo endpoint
        await axios.put(`${API_BASE}/responses/${alert.response_id}/undo`);
      } else {
        // Call block endpoint
        await axios.put(`${API_BASE}/responses/${alert.response_id}/block`);
      }
      fetchAlerts();
    } catch (err) {
      console.error("Error toggling block IP:", err);
    }
  };

  const handleToggleBlockUser = async (alert) => {
    try {
      if (alert.blockedUser) {
        // Call undo endpoint
        await axios.put(`${API_BASE}/responses/${alert.response_id}/undo`);
      } else {
        // Call block endpoint
        await axios.put(`${API_BASE}/responses/${alert.response_id}/block`);
      }
      fetchAlerts();
    } catch (err) {
      console.error("Error toggling block User:", err);
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-start bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black p-6">
      <h1 className="text-3xl font-extrabold dark:text-white text-black mb-8">
        Security Alerts
      </h1>

      <div className="w-full max-w-5xl space-y-4">
        {alertsData.map((alert, index) => (
          <motion.div
            key={alert.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05, duration: 0.4 }}
            className="bg-white dark:bg-zinc-900 rounded-xl p-4 shadow-md flex flex-col md:flex-row md:justify-between items-start md:items-center gap-4"
          >
            <div className="flex-1">
              <p className="font-semibold dark:text-white">
                {alert.alert_name}{" "}
                <span
                  className={`px-2 py-1 rounded-full text-xs ml-2 ${
                    alert.status === "suspended"
                      ? "bg-red-200 text-red-800 dark:bg-red-800 dark:text-red-200"
                      : "bg-green-200 text-green-800 dark:bg-green-800 dark:text-green-200"
                  }`}
                >
                  {alert.status}
                </span>
              </p>
              <p className="text-sm dark:text-gray-300">
                Confidence: {alert.confidence_score} | User: {alert.user_name} |
                IP: {alert.ip}
              </p>
              <p className="text-sm dark:text-gray-300">
                Email: {alert.email} | Device: {alert.device} | Action:{" "}
                {alert.action}
              </p>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => handleToggleBlockIP(alert)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  alert.blockedIP
                    ? "bg-red-600 text-white hover:bg-red-700"
                    : "bg-green-600 text-white hover:bg-green-700"
                }`}
              >
                {alert.blockedIP ? "Unblock IP" : "Block IP"}
              </button>

              <button
                onClick={() => handleToggleBlockUser(alert)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  alert.blockedUser
                    ? "bg-red-600 text-white hover:bg-red-700"
                    : "bg-green-600 text-white hover:bg-green-700"
                }`}
              >
                {alert.blockedUser ? "Unblock User" : "Block User"}
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
