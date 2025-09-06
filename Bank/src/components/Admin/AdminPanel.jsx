import React, { useState } from "react";
import { motion } from "framer-motion";

export function AdminPanel() {
  // Mock user list
  const [users, setUsers] = useState([
    { id: 1, name: "Alice Johnson", email: "alice@example.com", role: "user" },
    { id: 2, name: "Bob Smith", email: "bob@example.com", role: "user" },
    {
      id: 3,
      name: "Charlie Admin",
      email: "charlie@example.com",
      role: "admin",
    },
  ]);

  const [message, setMessage] = useState("");

  // Simulate delete
  const handleDelete = (id) => {
    setUsers(users.filter((u) => u.id !== id));
    setMessage(`User with ID ${id} deleted (mock).`);
    setTimeout(() => setMessage(""), 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black p-6">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="rounded-2xl bg-white dark:bg-zinc-950 shadow-lg p-6 max-w-3xl mx-auto"
      >
        <h2 className="text-2xl font-bold text-neutral-800 dark:text-neutral-100 mb-6">
          Admin Panel
        </h2>

        {message && (
          <div className="mb-4 p-3 rounded-lg bg-green-100 text-green-700 text-sm">
            {message}
          </div>
        )}

        {/* User list */}
        <div className="space-y-3">
          {users.length > 0 ? (
            users.map((user) => (
              <div
                key={user.id}
                className="flex justify-between items-center rounded-lg border border-neutral-200 dark:border-neutral-800 p-3"
              >
                <div>
                  <p className="text-sm font-medium text-neutral-800 dark:text-neutral-100">
                    {user.name} ({user.role})
                  </p>
                  <p className="text-xs text-neutral-500 dark:text-neutral-400">
                    {user.email}
                  </p>
                </div>
                <button
                  onClick={() => handleDelete(user.id)}
                  className="rounded-lg bg-red-500 px-3 py-1 text-white shadow hover:bg-red-600 transition"
                >
                  Delete
                </button>
              </div>
            ))
          ) : (
            <p className="text-sm text-neutral-500">No users available.</p>
          )}
        </div>
      </motion.div>
    </div>
  );
}
