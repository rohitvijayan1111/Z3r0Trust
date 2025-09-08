import React, { useState, useEffect } from "react";
import axios from "axios";
const backendUrl = import.meta.env.BACKEND;
export function AppealPage() {
  const [appealsData, setAppealsData] = useState([]);
  const [selectedAppeal, setSelectedAppeal] = useState(null);
  const API_BASE = `${backendUrl}/api`;

  useEffect(() => {
    fetchAppeals();
  }, []);

  const fetchAppeals = async () => {
    try {
      const res = await axios.get(`${API_BASE}/appeals`);
      setAppealsData(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Error fetching appeals:", err);
      setAppealsData([]);
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col items-center bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black p-6">
      <h1 className="text-3xl font-extrabold dark:text-white text-black mb-8">
        Appeals
      </h1>

      <div className="w-full max-w-5xl space-y-4">
        {appealsData.map((appeal, index) => (
          <div
            key={appeal.id}
            className="bg-white dark:bg-zinc-900 rounded-xl p-4 shadow-md flex flex-col md:flex-row md:justify-between items-start md:items-center gap-4"
          >
            <div className="flex-1">
              <p className="font-semibold dark:text-white">
                {appeal.subject || "No Subject"}{" "}
              </p>
              <p className="text-sm dark:text-gray-300">
                {appeal.content || "No Content"}
              </p>
            </div>
            <button
              onClick={() => setSelectedAppeal(appeal)}
              className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
            >
              View
            </button>
          </div>
        ))}
      </div>

      {/* Modal */}
      {selectedAppeal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-60 z-50">
          <div className="bg-white dark:bg-zinc-900 p-6 rounded-xl shadow-lg w-2/3 max-w-2xl">
            <h2 className="text-xl font-bold dark:text-white mb-2">
              Appeal Details
            </h2>
            <p className="dark:text-white">
              <strong>Subject:</strong> {selectedAppeal.subject}
            </p>
            <p className="dark:text-white mb-4">
              <strong>Content:</strong> {selectedAppeal.content}
            </p>

            {selectedAppeal.alert && (
              <>
                <hr className="my-4 border-gray-300 dark:border-zinc-700" />
                <h3 className="text-lg font-semibold dark:text-white">
                  Associated Alert
                </h3>
                <p className="dark:text-white">
                  <strong>Alert Name:</strong> {selectedAppeal.alert.alert_name}
                </p>
                <p className="dark:text-white">
                  <strong>Confidence:</strong>{" "}
                  {selectedAppeal.alert.confidence_score}
                </p>
                <p className="dark:text-white">
                  <strong>User:</strong> {selectedAppeal.alert.user}
                </p>
                <p className="dark:text-white">
                  <strong>IP:</strong> {selectedAppeal.alert.ip}
                </p>
                <p className="dark:text-white">
                  <strong>Device:</strong> {selectedAppeal.alert.device}
                </p>
                <p className="dark:text-white">
                  <strong>Status:</strong> {selectedAppeal.alert.status}
                </p>

                <div className="mt-4 flex gap-2">
                  <button
                    onClick={async () => {
                      try {
                        await axios.put(
                          `${API_BASE}/responses/${selectedAppeal.alert.id}/block_ip`
                        );
                        fetchAppeals();
                        setSelectedAppeal(null);
                      } catch (err) {
                        console.error("Error toggling IP:", err);
                      }
                    }}
                    className={`px-4 py-2 rounded-lg ${
                      selectedAppeal.alert.blockedIP
                        ? "bg-red-600 text-white"
                        : "bg-green-600 text-white"
                    }`}
                  >
                    {selectedAppeal.alert.blockedIP ? "Unblock IP" : "Block IP"}
                  </button>

                  <button
                    onClick={async () => {
                      try {
                        await axios.put(
                          `${API_BASE}/responses/${selectedAppeal.alert.id}/block_user`
                        );
                        fetchAppeals();
                        setSelectedAppeal(null);
                      } catch (err) {
                        console.error("Error toggling User:", err);
                      }
                    }}
                    className={`px-4 py-2 rounded-lg ${
                      selectedAppeal.alert.blockedUser
                        ? "bg-red-600 text-white"
                        : "bg-green-600 text-white"
                    }`}
                  >
                    {selectedAppeal.alert.blockedUser
                      ? "Unblock User"
                      : "Block User"}
                  </button>
                </div>
              </>
            )}

            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setSelectedAppeal(null)}
                className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
