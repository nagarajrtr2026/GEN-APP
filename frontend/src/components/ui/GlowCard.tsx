import React from 'react';
import { motion } from 'framer-motion';

export const GlowCard: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => {
  return (
    <motion.div 
      whileHover={{ y: -5 }}
      className={`relative rounded-xl p-0.5 bg-gradient-to-br from-white/10 to-transparent group ${className}`}
    >
      <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-accent-cyan to-accent-violet opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-sm" />
      <div className="relative h-full w-full bg-dark-800 rounded-xl glass p-6 z-10 overflow-hidden">
        {children}
      </div>
    </motion.div>
  );
};