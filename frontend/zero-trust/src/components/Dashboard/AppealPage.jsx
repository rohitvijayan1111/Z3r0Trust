import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import axios from "axios";

export function AppealPage() {
  const [appeals, setAppeals] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [selectedAppeal, setSelectedAppeal] = useState(null);
  const API_BASE = "http://127.0.0.1:5000/api";

  useEffect(() => {
    fetchAppeals();
    fetchAlerts();
  }, []);

  const fetchAppeals = async () => {
    try {
      const res = await axios.get(`${API_BASE}/appeals`);
      setAppeals(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Error fetching appeals:", err);
      setAppeals([]);
    }
  };

  const fetchAlerts = async () => {
    try {
      const res = await axios.get(`${API_BASE}/alerts`);
      setAlerts(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Error fetching alerts:", err);
      setAlerts([]);
    }
  };

  const handleBlock = async (responseId) => {
    try {
      await axios.put(`${API_BASE}/responses/${responseId}/block`);
      alert("Response & associated alert blocked successfully!");
      fetchAppeals();
      fetchAlerts();
      setSelectedAppeal(null);
    } catch (err) {
      console.error("Error blocking response:", err);
      alert("Failed to block response.");
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-start bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black px-4 sm:px-6 lg:px-12 py-12">
      <h1 className="text-1xl sm:text-3xl font-extrabold dark:text-white text-black mb-6">
        Appeals
      </h1>

      {/* Appeals Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="w-full max-w-5xl overflow-x-auto mb-12"
      >
        <table className="min-w-full divide-y divide-gray-200 dark:divide-zinc-700 rounded-xl overflow-hidden">
          <thead className="bg-gray-200 dark:bg-zinc-800">
            <tr>
              {["ID", "Subject", "Content", "View"].map((header) => (
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
            {appeals.map((appeal, index) => (
              <motion.tr
                key={appeal.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05, duration: 0.4 }}
                className="hover:bg-gray-50 dark:hover:bg-zinc-800 transition"
              >
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {appeal.id}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {appeal.subject}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {appeal.content}
                </td>
                <td className="px-4 py-3">
                  <button
                    onClick={() => setSelectedAppeal(appeal)}
                    className="px-3 py-1 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                  >
                    View
                  </button>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </motion.div>

      {/* Alerts Table */}
      <h1 className="text-1xl sm:text-3xl font-extrabold dark:text-white text-black mb-6">
        Alerts
      </h1>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="w-full max-w-5xl overflow-x-auto"
      >
        <table className="min-w-full divide-y divide-gray-200 dark:divide-zinc-700 rounded-xl overflow-hidden">
          <thead className="bg-gray-200 dark:bg-zinc-800">
            <tr>
              {[
                "ID",
                "Alert Name",
                "Confidence",
                "User",
                "Email",
                "IP",
                "Blocked IP",
                "Blocked User",
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
            {alerts.map((alert, index) => (
              <motion.tr
                key={alert.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05, duration: 0.4 }}
                className="hover:bg-gray-50 dark:hover:bg-zinc-800 transition"
              >
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.id}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.alert_name}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.confidence_score}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.user_name}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.email}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.ip}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.blockedIP ? "Yes" : "No"}
                </td>
                <td className="px-4 py-3 text-sm text-black dark:text-white">
                  {alert.blockedUser ? "Yes" : "No"}
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </motion.div>

      {/* Modal for Appeal Details */}
      {selectedAppeal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-zinc-900 p-6 rounded-xl w-11/12 max-w-2xl relative"
          >
            <h2 className="text-xl font-bold dark:text-white mb-4">
              Appeal Details
            </h2>
            <p className="dark:text-white">
              <strong>Subject:</strong> {selectedAppeal.subject}
            </p>
            <p className="dark:text-white">
              <strong>Content:</strong> {selectedAppeal.content}
            </p>

            {selectedAppeal.response && (
              <>
                <hr className="my-4 border-gray-300 dark:border-zinc-700" />
                <h3 className="text-lg font-semibold dark:text-white">
                  Associated Response
                </h3>
                <p className="dark:text-white">
                  <strong>Alert Name:</strong>{" "}
                  {selectedAppeal.response.alert_name}
                </p>
                <p className="dark:text-white">
                  <strong>Confidence Score:</strong>{" "}
                  {selectedAppeal.response.confidence_score}
                </p>
                <p className="dark:text-white">
                  <strong>Status:</strong> {selectedAppeal.response.status}
                </p>
                {console.log(
                  "Response status:",
                  selectedAppeal.response.status
                )}

                {/* Block / Unblock Buttons */}
                {selectedAppeal.response.status === "suspended" ? (
                  <button
                    onClick={async () => {
                      try {
                        await axios.put(
                          `${API_BASE}/responses/${selectedAppeal.response.id}/undo`
                        );
                        alert(
                          "Response & associated alert unblocked successfully!"
                        );
                        fetchAppeals();
                        fetchAlerts();
                        setSelectedAppeal(null);
                      } catch (err) {
                        console.error("Error unblocking response:", err);
                        alert("Failed to unblock response.");
                      }
                    }}
                    className="mt-4 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
                  >
                    Unblock
                  </button>
                ) : (
                  <button
                    onClick={() => handleBlock(selectedAppeal.response.id)}
                    className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
                  >
                    Block
                  </button>
                )}
              </>
            )}
            <button
              onClick={() => setSelectedAppeal(null)}
              className="mt-6 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition"
            >
              Close
            </button>
          </motion.div>
        </div>
      )}
    </div>
  );
}
