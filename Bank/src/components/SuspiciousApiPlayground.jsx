import React, { useState } from "react";
import { motion } from "framer-motion";

export function SuspiciousApiPlayground() {
  const [payload, setPayload] = useState("");
  const [response, setResponse] = useState(null);

  const handleEcho = () => {
    try {
      setResponse(JSON.parse(payload));
    } catch {
      setResponse({ error: "Invalid JSON payload" });
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-2xl bg-white dark:bg-zinc-950 p-6 rounded-2xl shadow-lg"
      >
        <h2 className="text-xl font-bold mb-4 dark:text-white">
          Suspicious API Playground
        </h2>
        <textarea
          className="w-full h-32 rounded-lg border dark:border-neutral-700 p-3 font-mono text-sm dark:bg-zinc-900 dark:text-white"
          placeholder="Enter JSON payload here..."
          value={payload}
          onChange={(e) => setPayload(e.target.value)}
        />
        <button
          onClick={handleEcho}
          className="mt-4 w-full rounded-lg bg-green-600 text-white py-2 hover:bg-green-700"
        >
          Send to Echo API →
        </button>
        {response && (
          <pre className="mt-4 bg-gray-100 dark:bg-zinc-800 p-3 rounded-lg text-sm text-left overflow-x-auto">
            {JSON.stringify(response, null, 2)}
          </pre>
        )}
      </motion.div>
    </div>
  );
}
