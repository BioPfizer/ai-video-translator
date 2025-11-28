"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { useDropzone } from "react-dropzone";
import { cn } from "@/lib/utils";

interface FileUploadProps {
  onChange?: (file: File | null) => void;
}

export const FileUpload = ({ onChange }: FileUploadProps) => {
  const [file, setFile] = useState<File | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "video/*": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      console.log('onDrop triggered, files:', acceptedFiles);
      if (acceptedFiles.length > 0) {
        const selectedFile = acceptedFiles[0];
        console.log('Setting file:', selectedFile.name);
        setFile(selectedFile);
        onChange?.(selectedFile);
      }
    },
  });

  const handleRemove = (e: React.MouseEvent) => {
    e.stopPropagation();
    console.log('Removing file');
    setFile(null);
    onChange?.(null);
  };

  return (
    <div className="w-full">
      {/* Animation wrapper - doesn't interfere with dropzone */}
      <motion.div
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.99 }}
        transition={{ duration: 0.2 }}
        className="relative"
      >
        {/* Functional dropzone */}
        <div
          {...getRootProps()}
          className={cn(
            "relative group/file block rounded-lg cursor-pointer w-full",
            "border-2 border-dashed transition-all duration-300 p-10",
            isDragActive
              ? "border-cyan-500 bg-cyan-500/10"
              : "border-slate-700 hover:border-slate-600 bg-slate-800/50"
          )}
        >
          <input {...getInputProps()} />
        
          <div className="text-center">
            {!file ? (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                {/* Upload Icon */}
                <div className="flex justify-center mb-4">
                  <svg
                    className={cn(
                      "w-16 h-16 transition-colors",
                      isDragActive ? "text-cyan-500" : "text-slate-500"
                    )}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                    />
                  </svg>
                </div>

                {/* Text */}
                <p className="text-lg font-semibold text-slate-200 mb-2">
                  {isDragActive ? "Drop your video here" : "Drag & drop video file"}
                </p>
                <p className="text-sm text-slate-400 mb-4">
                  or click to browse
                </p>
                <p className="text-xs text-slate-500">
                  Supports: MP4, MOV, AVI, MKV, WEBM (Max 100MB)
                </p>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
                className="space-y-4"
              >
                {/* File Icon */}
                <div className="flex justify-center">
                  <div className="w-16 h-16 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl flex items-center justify-center">
                    <svg
                      className="w-8 h-8 text-white"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                      />
                    </svg>
                  </div>
                </div>

                {/* File Info */}
                <div>
                  <p className="text-lg font-semibold text-slate-200 truncate">
                    {file.name}
                  </p>
                  <p className="text-sm text-slate-400 mt-1">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>

                {/* Remove Button */}
                <motion.button
                  onClick={handleRemove}
                  className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg text-sm font-medium transition-colors"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Remove
                </motion.button>
              </motion.div>
            )}
          </div>
        </div>

        {/* Animated border gradient on drag */}
        {isDragActive && (
          <motion.div
            className="absolute inset-0 rounded-lg pointer-events-none"
            style={{
              background:
                "linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.3), transparent)",
              backgroundSize: "200% 100%",
            }}
            animate={{
              backgroundPosition: ["0% 50%", "200% 50%"],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "linear",
            }}
          />
        )}
      </motion.div>
    </div>
  );
};