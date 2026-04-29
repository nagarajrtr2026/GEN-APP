import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

export const EmptyPreviewState = () => {
  const navigate = useNavigate();
  return (
    <div className="h-screen w-full flex flex-col items-center justify-center bg-dark-900 text-white">
      <motion.div 
        initial={{ scale: 0.9, opacity: 0 }} 
        animate={{ scale: 1, opacity: 1 }} 
        className="text-center"
      >
        <div className="w-20 h-20 bg-dark-800 rounded-full flex items-center justify-center mx-auto mb-6 border border-white/10 shadow-[0_0_30px_rgba(6,182,212,0.3)]">
          <Sparkles className="text-accent-cyan" size={32} />
        </div>
        <h2 className="text-2xl font-bold mb-2">No Schema Generated</h2>
        <p className="text-gray-400 mb-8 max-w-md mx-auto">Please generate an application architecture from the dashboard first to view the live preview.</p>
        <button 
          onClick={() => navigate('/dashboard')}
          className="px-6 py-3 bg-accent-violet hover:bg-accent-cyan text-white rounded-lg font-medium transition-colors shadow-lg shadow-accent-violet/20"
        >
          Go to Dashboard
        </button>
      </motion.div>
    </div>
  );
};