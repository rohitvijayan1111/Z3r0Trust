import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

const projectMessages = [
  "Proactively detects suspicious traffic before it impacts your systems.",
  "Enforces security measures automatically to protect sessions.",
  "Generates actionable insights from all incoming logs in real-time.",
  "Alerts you with risk scores and recommended actions instantly.",
  "Monitors user activity and prevents unauthorized access seamlessly.",
];


export function FloatingMessages() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      const randomMessage =
        projectMessages[Math.floor(Math.random() * projectMessages.length)];
      const id = Date.now();
      const top = Math.random() * 80; // vertical position
      const left = Math.random() * 70; // horizontal position

      setMessages((prev) => [...prev, { id, text: randomMessage, top, left }]);

      setTimeout(() => {
        setMessages((prev) => prev.filter((msg) => msg.id !== id));
      }, 4000);
    }, 2500); // slightly slower interval for readability

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none z-50">
      <AnimatePresence>
        {messages.map((msg) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, scale: 0.8, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -10 }}
            style={{ top: `${msg.top}%`, left: `${msg.left}%` }}
            className="absolute max-w-xs p-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-mono text-sm rounded-2xl shadow-xl border border-purple-400/30 backdrop-blur-md"
          >
            {msg.text}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
