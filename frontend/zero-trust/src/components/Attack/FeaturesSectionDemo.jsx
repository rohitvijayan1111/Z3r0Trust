import { cn } from "../../lib/utils";
import { motion } from "framer-motion";
import {
  IconShieldCheck,
  IconAlertCircle,
  IconLock,
  IconDeviceLaptop,
  IconServer,
  IconUserCheck,
} from "@tabler/icons-react";
import { useState } from "react";
const backendUrl = import.meta.env.BACKEND;
export function FeaturesSectionDemo() {
  const [loading, setLoading] = useState(null);
  const [response, setResponse] = useState(null);

  const API_BASE = `${backendUrl}/api/payloads`;

  const agents = [
    {
      title: "Analyzer Agent",
      examples: [
        {
          riskType: "Brute Force / Credential Abuse",
          endpoint: `${API_BASE}/password_bruteforce`,
          icon: <IconLock className="w-8 h-8 text-red-500" />,
        },
        {
          riskType: "Credential Stuffing",
          endpoint: `${API_BASE}/credential_stuffing`,
          icon: <IconDeviceLaptop className="w-8 h-8 text-purple-500" />,
        },
        {
          riskType: "Impossible Travel / Account Takeover",
          endpoint: `${API_BASE}/simulate_impossible_travel`,
          icon: <IconServer className="w-8 h-8 text-yellow-400" />,
        },
        {
          riskType: "Bot/Malware Detection",
          endpoint: `${API_BASE}/malware_bot_behaviour`,
          icon: <IconUserCheck className="w-8 h-8 text-blue-400" />,
        },
        {
          riskType: "Privilege Escalation",
          endpoint: `${API_BASE}/privilege_escalation`,
          icon: <IconAlertCircle className="w-8 h-8 text-orange-400" />,
        },
        {
          riskType: "Suspicious API / Data Exfiltration",
          endpoint: `${API_BASE}/data_exfiltration`,
          icon: <IconShieldCheck className="w-8 h-8 text-green-400" />,
        },
        {
          riskType: "Network Anomalies",
          endpoint: `${API_BASE}/network_anomalies`,
          icon: <IconShieldCheck className="w-8 h-8 text-pink-500" />,
        },
      ],
    },
  ];

  // Call API when button is clicked
  const handleBeginClick = async (endpoint) => {
    setLoading(endpoint);
    setResponse(null);
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        credentials: "include",
      });
      const data = await res.json();
      setResponse({ endpoint, data });
    } catch (err) {
      console.error(err);
      setResponse({ endpoint, data: { error: err.message } });
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-900 to-black p-6">
      <div className="max-w-7xl mx-auto space-y-12">
        {agents.map((agent) => (
          <div key={agent.title}>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
              {agent.examples.map((item, idx) => (
                <motion.div
                  key={idx}
                  className="bg-gradient-to-br from-zinc-900 to-zinc-800 rounded-2xl p-6 flex flex-col justify-between shadow-lg hover:shadow-2xl transition-all duration-300 border-l-4 border-transparent hover:border-blue-500"
                  whileHover={{ scale: 1.05 }}
                >
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3">
                      {item.icon}
                      <h3 className="font-bold text-lg text-neutral-100">
                        {item.riskType}
                      </h3>
                    </div>
                  </div>
                  <button
                    className="mt-4 rounded-md bg-gradient-to-br from-black to-neutral-600 px-4 py-2 text-white font-medium shadow-md hover:opacity-90 dark:from-zinc-800 dark:to-zinc-700 transition"
                    onClick={() => handleBeginClick(item.endpoint)}
                  >
                    {loading === item.endpoint ? "Processing..." : "Begin"}
                  </button>
                </motion.div>
              ))}
            </div>
          </div>
        ))}

        {/* Show last API response */}
        {response && (
          <pre className="mt-6 p-4 bg-zinc-900 text-green-400 rounded-lg overflow-x-auto">
            {JSON.stringify(response, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
