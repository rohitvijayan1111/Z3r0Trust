import React from "react";
import { EvervaultCard, Icon } from "../ui/evervault-card";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export function EvervaultCardDemo() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-gray-200 dark:from-zinc-900 dark:to-black px-4 sm:px-6 lg:px-12 py-12 relative">
      {/* Top-left Lock Icon */}
      <div className="absolute top-6 left-6 z-50">
        <img src="lock.png" alt="lock" className="w-8 h-8" />
      </div>

      {/* Cards */}
      <div className="flex flex-col sm:flex-row gap-8 justify-center items-center w-full max-w-6xl">
        <CardWrapper
          title="Alerts"
          description="Stay informed with instant security alerts to keep your data protected."
          buttonText="Show Alerts"
          route="/alerts"
        />
        <CardWrapper
          title="Responses"
          description="Easily manage and respond to notifications with one click."
          buttonText="Get Responses"
          route="/responses"
        />
        <CardWrapper
          title="Appeal"
          description="Submit or track appeals for any alerts or responses easily."
          buttonText="Go to Appeal"
          route="/appeal"
        />
      </div>
    </div>
  );
}

/* Shared Card Component */
const CardWrapper = ({ title, description, buttonText, route }) => {
  const navigate = useNavigate();

  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className="flex flex-col items-start w-full sm:w-1/3 max-w-sm p-6 relative rounded-xl bg-white/5 dark:bg-zinc-900/50 backdrop-blur-md shadow-lg border border-black/[0.2] dark:border-white/[0.2]"
    >
      {/* Corners */}
      <Icon className="absolute h-6 w-6 -top-3 -left-3 dark:text-white text-black" />
      <Icon className="absolute h-6 w-6 -bottom-3 -left-3 dark:text-white text-black" />
      <Icon className="absolute h-6 w-6 -top-3 -right-3 dark:text-white text-black" />
      <Icon className="absolute h-6 w-6 -bottom-3 -right-3 dark:text-white text-black" />

      {/* Card Content */}
      <EvervaultCard text={title} className="w-full h-48 sm:h-60" />
      <h2 className="dark:text-white text-black mt-4 text-xl sm:text-2xl font-semibold">
        {title}
      </h2>
      <p className="dark:text-neutral-300 text-neutral-700 mt-2 text-sm sm:text-base font-light">
        {description}
      </p>
      <motion.button
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.97 }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
        onClick={() => navigate(route)}
        className="text-sm sm:text-base border font-medium dark:border-white/[0.2] border-black/[0.2] rounded-full mt-6 text-black dark:text-white px-4 py-2 hover:bg-black/10 dark:hover:bg-white/10 transition"
      >
        {buttonText}
      </motion.button>
    </motion.div>
  );
};
