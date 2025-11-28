"use client";
import React from "react";
import { motion } from "framer-motion";
import { BackgroundRippleEffect } from "@/components/ui/background-ripple-effect";

export const BackgroundRipple = () => {
    return (
         <div className="absolute inset-0 overflow-hidden">
            {/* Animated gradient background */}
            <div className="absolute inset-0 bg-gradient-to-br from-slate-900 to-slate-900" />
            <BackgroundRippleEffect />

            {/* Ripple circles */}
            <motion.div
                className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"
                animate={{
                scale: [1, 1.2, 1],
                opacity: [0.3, 0.5, 0.3],
                }}
                transition={{
                duration: 8,
                repeat: Infinity,
                ease: "easeInOut",
                }}
            />
            
            <motion.div
                className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"
                animate={{
                scale: [1.2, 1, 1.2],
                opacity: [0.5, 0.3, 0.5],
                }}
                transition={{
                duration: 10,
                repeat: Infinity,
                ease: "easeInOut",
                }}
            />
            
            <motion.div
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"
                animate={{
                scale: [1, 1.3, 1],
                opacity: [0.4, 0.6, 0.4],
                }}
                transition={{
                duration: 12,
                repeat: Infinity,
                ease: "easeInOut",
                }}
            />

            
      {/* Grid overlay */}
      <div className="absolute inset-0 bg-grid-slate-700"/>
    </div>
    );
};