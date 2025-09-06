import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ApiIntegrationForm } from "./ApiIntegrationForm";

export function IntegrationSidebar() {
  const [activeTab, setActiveTab] = useState("integration");

  return (
    <div className="flex min-h-screen bg-black text-gray-300">
      {/* Sidebar */}
      <aside className="w-72 bg-[#0a0a0a]/95 border-r border-[#1a1a1a] flex flex-col">
        <h2 className="text-2xl font-bold p-6 text-white tracking-wide flex items-center gap-2">
          ⚡ Security Panel
        </h2>
        <nav className="flex flex-col space-y-2 px-4">
          {[
            { key: "integration", label: "🔗 Integration" },
            { key: "docs", label: "📖 Documentation" },
          ].map((item) => (
            <button
              key={item.key}
              onClick={() => setActiveTab(item.key)}
              className={`text-left px-5 py-3 rounded-xl font-medium transition-all ${
                activeTab === item.key
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-500/30"
                  : "hover:bg-[#111] hover:text-indigo-400"
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto bg-black">
        <AnimatePresence mode="wait">
          {activeTab === "integration" && (
            <motion.div
              key="integration"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="flex justify-center"
            >
              <ApiIntegrationForm />
            </motion.div>
          )}

          {activeTab === "docs" && (
            <motion.div
              key="docs"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="max-w-3xl mx-auto bg-[#0a0a0a]/95 border border-[#1a1a1a] rounded-2xl p-8 shadow-lg shadow-black/50"
            >
              <h2 className="text-3xl font-bold text-white mb-6">
                📖 How to Send Logs
              </h2>
              <p className="text-gray-400 mb-6 leading-relaxed">
                Use the following{" "}
                <span className="text-indigo-400 font-semibold">FastAPI</span>{" "}
                endpoint to send login events. Forward logs in this format:
              </p>

              <CodeBlock
                code={`POST /login-with-email
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword",
  "request_type": "login"
}`}
                color="text-green-400"
              />

              <h3 className="text-xl font-semibold text-white mt-8 mb-3">
                ✅ Successful Response
              </h3>
              <CodeBlock
                code={`{
  "status": "success",
  "attributes": {
    "Timestamp": 1725629472,
    "Username": "user@example.com",
    "IP Address": "103.25.123.45",
    "Geo Location": "IN/Tamil Nadu/Chennai",
    "Device": "Chrome 116 on Windows 10 (Desktop)",
    "Request type": "login",
    "Response": "success"
  },
  "session_jwt": "xxxxxx"
}`}
                color="text-blue-400"
              />

              <h3 className="text-xl font-semibold text-white mt-8 mb-3">
                ❌ Failure Response
              </h3>
              <CodeBlock
                code={`{
  "status": "failure",
  "message": "Invalid credentials",
  "attributes": {
    "Timestamp": 1725629490,
    "IP Address": "103.25.123.45",
    "Geo Location": "IN/Tamil Nadu/Chennai",
    "Device": "Chrome 116 on Windows 10 (Desktop)",
    "Request type": "login",
    "Response": "failure"
  }
}`}
                color="text-red-400"
              />
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

// Reusable Code Block
function CodeBlock({ code, color }) {
  return (
    <pre
      className={`bg-[#111]/90 p-4 rounded-xl text-sm ${color} overflow-x-auto border border-[#222] shadow-inner shadow-black/40`}
    >
      {code}
    </pre>
  );
}
