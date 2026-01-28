import React from 'react';
import { Mic, Square } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const AudioRecorder = ({ isRecording, onToggle }) => {
  return (
    <button 
      onClick={onToggle}
      className={`relative p-3 rounded-xl transition-all duration-300 ${
        isRecording 
          ? "bg-rose-500 text-white shadow-lg shadow-rose-200" 
          : "bg-slate-50 text-slate-500 hover:bg-slate-100"
      }`}
    >
      <AnimatePresence mode="wait">
        {isRecording ? (
          <motion.div
            key="recording"
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.5, opacity: 0 }}
          >
            <Square size={24} fill="currentColor" />
          </motion.div>
        ) : (
          <motion.div
            key="idle"
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.5, opacity: 0 }}
          >
            <Mic size={24} />
          </motion.div>
        )}
      </AnimatePresence>

      {isRecording && (
        <span className="absolute -top-1 -right-1 flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
        </span>
      )}
    </button>
  );
};

export default AudioRecorder;
