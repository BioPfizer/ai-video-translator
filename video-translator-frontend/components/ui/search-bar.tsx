"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface SearchBarProps {
    placeholder?: string;
    value: string;
    onChange: (value: string) => void;
    onSubmit?: () => void;
}

export const SearchBar = ({
  placeholder = "Paste YouTube, TikTok, or Instagram URL...",
  value,
  onChange,
  onSubmit,
}: SearchBarProps) => {
  const [isFocused, setIsFocused] = useState(false);

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && onSubmit) {
      onSubmit();
    }
  };

  return (
    <motion.div
      className="relative w-full"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Animated gradient background */}
      <motion.div
        className={cn(
          "absolute -inset-1 rounded-lg bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 opacity-0 blur transition-opacity duration-500",
          isFocused && "opacity-30"
        )}
      />

      {/* Search bar container */}
      <div className="relative flex items-center bg-slate-800/90 backdrop-blur-xl rounded-lg border border-slate-700 overflow-hidden">
        {/* Search icon */}
        <div className="pl-4 pr-3">
          <motion.svg
            className={cn(
              "w-5 h-5 transition-colors",
              isFocused ? "text-cyan-400" : "text-slate-500"
            )}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            animate={isFocused ? { rotate: [0, 10, 0] } : {}}
            transition={{ duration: 0.3 }}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 10a1 1 0 011-1h4a1 1 0 110 2h-4a1 1 0 01-1-1z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 14a1 1 0 011-1h2a1 1 0 110 2h-2a1 1 0 01-1-1z"
            />
          </motion.svg>
        </div>

        {/* Input field */}
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          className={cn(
            "flex-1 py-4 pr-4 bg-transparent text-slate-200 placeholder-slate-500",
            "focus:outline-none text-base"
          )}
        />

        {/* Clear button */}
        {value && (
          <motion.button
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            onClick={() => onChange("")}
            className="mr-2 p-2 hover:bg-slate-700 rounded-lg transition-colors"
          >
            <svg
              className="w-4 h-4 text-slate-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </motion.button>
        )}
      </div>

      {/* Helper text */}
      <motion.p
        className="mt-2 text-xs text-slate-500 px-1"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        Supports YouTube Shorts, TikTok, and Instagram Reels
      </motion.p>
    </motion.div>
  );
};