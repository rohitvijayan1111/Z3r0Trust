import React, { useState } from "react";
import { motion } from "framer-motion";

export function NetworkAnomalySimulation() {
  const [logs, setLogs] = useState([]);

  const pingHealth = () => {
    setLogs((prev) => [
      ...prev,
      { time: new Date().toLocaleTimeString(), status: "200 OK" },
    ]);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-lg bg-white dark:bg-zinc-950 p-6 rounded-2xl shadow-lg"
      >
        <h2 className="text-xl font-bold mb-4 dark:text-white">
          Network Anomaly Simulation
        </h2>
        <button
          onClick={pingHealth}
          className="w-full rounded-lg bg-purple-600 text-white py-2 hover:bg-purple-700"
        >
          Ping /health →
        </button>
        <div className="mt-4 space-y-2 max-h-64 overflow-y-auto">
          {logs.map((log, idx) => (
            <div
              key={idx}
              className="flex justify-between bg-gray-100 dark:bg-zinc-800 rounded-lg p-2 text-sm"
            >
              <span>{log.time}</span>
              <span className="text-green-600">{log.status}</span>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
