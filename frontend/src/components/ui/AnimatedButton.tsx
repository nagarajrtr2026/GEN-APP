import React from 'react';
import { motion } from 'framer-motion';

export const AnimatedButton: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' }> = ({ children, variant = 'primary', className = '', ...props }) => {
  const isPrimary = variant === 'primary';
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`relative px-6 py-3 rounded-lg font-medium overflow-hidden group ${isPrimary ? 'bg-accent-violet text-white' : 'bg-transparent text-white border border-white/20'} ${className}`}
      {...props}
    >
      {isPrimary && (
        <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-accent-cyan to-accent-violet opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      )}
      <span className="relative z-10">{children}</span>
    </motion.button>
  );
};