import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { HoverBorderGradient } from "../ui/hover-border-gradient";

export function HoverBorderGradientDemo() {
  const [isExiting, setIsExiting] = useState(false);
  const navigate = useNavigate();

  const handleClick = () => {
    setIsExiting(true); // trigger exit animation
    setTimeout(() => {
      navigate("/userAuth");
    }, 600); // wait for animation before navigating
  };

  return (
    <>
      <div className="flex justify-center text-center relative">
        <HoverBorderGradient
          containerClassName="rounded-full"
          as="button"
          className="dark:bg-black bg-white text-black dark:text-white flex items-center space-x-2"
          onClick={handleClick}
        >
          <AceternityLogo />
          <span>Get Started</span>
        </HoverBorderGradient>

        {/* Exit animation overlay */}
        <AnimatePresence>
          {isExiting && (
            <motion.div
              className="fixed inset-0 z-[9999] bg-black"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.6, ease: "easeInOut" }}
            />
          )}
        </AnimatePresence>
      </div>
    </>
  );
}

const AceternityLogo = () => (
  <svg
    width="66"
    height="65"
    viewBox="0 0 66 65"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className="h-3 w-3 text-black dark:text-white"
  >
    <path
      d="M8 8.05571C8 8.05571 54.9009 18.1782 57.8687 30.062C60.8365 41.9458 9.05432 57.4696 9.05432 57.4696"
      stroke="currentColor"
      strokeWidth="15"
      strokeMiterlimit="3.86874"
      strokeLinecap="round"
    />
  </svg>
);
