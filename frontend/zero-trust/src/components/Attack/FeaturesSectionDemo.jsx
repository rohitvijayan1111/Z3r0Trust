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

export function FeaturesSectionDemo() {
  const agents = [
    {
      title: "Analyzer Agent",
      description:
        "The Analyzer Agent takes flagged events, assesses risk, correlates with other data, and recommends mitigation.",
      examples: [
        {
          riskType: "Brute Force / Credential Abuse",
          correlation:
            "Compute risk score based on # failed attempts & history",
          action: "Risk = High if >50 failed logins",
          simulation: "Example: 3 failed logins + 1 unusual IP = medium risk",
          icon: <IconLock className="w-8 h-8 text-red-500" />,
        },
        {
          riskType: "Impossible Travel / Account Takeover",
          correlation: "Check geolocation, device fingerprint, session history",
          action: "Risk = High if IP jump >5000 km in <1 hour",
          simulation:
            "Example: unusual login from another country triggers alert",
          icon: <IconDeviceLaptop className="w-8 h-8 text-purple-500" />,
        },
        {
          riskType: "Bot/Malware Detection",
          correlation: "Compare request patterns to normal behavior",
          action: "Risk = Medium if >100 rapid requests",
          simulation: "Example: high frequency API calls from same IP",
          icon: <IconServer className="w-8 h-8 text-yellow-400" />,
        },
        {
          riskType: "Privilege Escalation",
          correlation: "Check user roles and access patterns",
          action: "Suggest review by security team",
          simulation: "Example: User suddenly granted admin rights",
          icon: <IconUserCheck className="w-8 h-8 text-blue-400" />,
        },
        {
          riskType: "Suspicious API / Data Exfiltration",
          correlation: "Check for large downloads, repetitive requests",
          action: "Risk = High if >500MB downloaded from sensitive endpoints",
          simulation: "Example: multiple downloads of confidential reports",
          icon: <IconAlertCircle className="w-8 h-8 text-orange-400" />,
        },
        {
          riskType: "Internal Misuse",
          correlation: "Cross-check with normal employee behavior",
          action: "Combine multiple low-risk events into higher-risk alert",
          simulation:
            "Example: Employee accessing sensitive files at odd hours",
          icon: <IconShieldCheck className="w-8 h-8 text-green-400" />,
        },
        {
          riskType: "Correlation Alert",
          correlation:
            "Combine multiple low-risk events into a higher-risk alert",
          action: "Risk = Medium if multiple small anomalies detected",
          simulation: "Example: 3 failed logins + 1 unused IP = medium risk",
          icon: <IconShieldCheck className="w-8 h-8 text-pink-500" />,
        },
      ],
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-900 to-black">
      {/* Navbar */}
      <div className="top-0 left-0 w-full shadow-md z-50">
        <div className="">
          <img src="logo.png" alt="logo" className="w-50 h-45 py-2 px-2" />
        </div>
      </div>

      {/* Agents Section */}
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
                    <p className="text-neutral-400 text-sm">
                      <span className="font-semibold">Correlation:</span>{" "}
                      {item.correlation}
                    </p>
                    <p className="text-neutral-400 text-sm">
                      <span className="font-semibold">Analyzer Action:</span>{" "}
                      {item.action}
                    </p>
                    <p className="text-neutral-400 text-sm">
                      <span className="font-semibold">Example Simulation:</span>{" "}
                      {item.simulation}
                    </p>
                  </div>
                  <button className="mt-4 rounded-md bg-gradient-to-br from-black to-neutral-600 px-4 py-2 text-white font-medium shadow-md hover:opacity-90 dark:from-zinc-800 dark:to-zinc-700 transition">
                    Begin
                  </button>
                </motion.div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
