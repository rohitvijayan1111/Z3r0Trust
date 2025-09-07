import React, { useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";

export function ApiIntegrationForm() {
  const [clientName, setClientName] = useState("");
  const [clientUrl, setClientUrl] = useState("");
  const [proxyUrl, setProxyUrl] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/proxies/add", {
        client_name: clientName,
        client_url: clientUrl,
      });
      setProxyUrl(res.data.proxy_url);
      setMessage("✅ API Integrated Successfully!");
    } catch (err) {
      setMessage("❌ Integration Failed: " + err.response?.data?.error);
    }
  };

  return (
    <motion.div
      className="flex items-center justify-center w-full"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <motion.form
        onSubmit={handleSubmit}
        className="w-full max-w-lg bg-gray-900/90 backdrop-blur-lg rounded-2xl shadow-2xl p-10 space-y-6 border border-gray-800"
        initial={{ y: 40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.4 }}
      >
        {/* Title */}
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-extrabold text-white">
            🔐 API Security Integration
          </h2>
          <p className="text-gray-400 text-sm">
            Connect your API with our{" "}
            <span className="text-indigo-400">Zero Trust</span>
          </p>
        </div>

        {/* Client Name */}
        <div className="space-y-2">
          <label className="text-gray-300 text-sm font-medium">
            Client Name
          </label>
          <input
            type="text"
            placeholder="Example Corp"
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            className="w-full p-3 rounded-xl bg-gray-950/80 border border-gray-700 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        {/* Client URL */}
        <div className="space-y-2">
          <label className="text-gray-300 text-sm font-medium">
            Client URL
          </label>
          <input
            type="text"
            placeholder="https://client.com/api"
            value={clientUrl}
            onChange={(e) => setClientUrl(e.target.value)}
            className="w-full p-3 rounded-xl bg-gray-950/80 border border-gray-700 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold py-3 rounded-xl shadow-lg shadow-indigo-600/30 transition-all"
        >
          🚀 Integrate API
        </button>

        {/* Show Result */}
        {message && <p className="text-center text-gray-300 mt-4">{message}</p>}
        {proxyUrl && (
          <div className="bg-gray-800 p-4 rounded-lg mt-3 text-indigo-400 text-center">
            Your Proxy URL: <br />
            <span className="font-mono">{proxyUrl}</span>
          </div>
        )}
      </motion.form>
    </motion.div>
  );
}
