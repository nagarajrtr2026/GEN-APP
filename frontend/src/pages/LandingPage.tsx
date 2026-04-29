import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { AnimatedButton } from '../components/ui/AnimatedButton';
import { Zap, Code, Database, Sparkles } from 'lucide-react';

export const LandingPage = () => {
  return (
    <><div className="min-h-screen flex flex-col items-center pt-32 px-4 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-accent-violet/30 rounded-full blur-[120px] animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-cyan/30 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '2s' }} />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center z-10 max-w-4xl"
      >
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 mb-8 backdrop-blur-md">
          <Sparkles size={16} className="text-accent-cyan" />
          <span className="text-sm text-gray-300">Gen-Ora AI is live</span>
        </div>

        <h1 className="text-6xl md:text-8xl font-black mb-6 tracking-tight">
          Design software at the speed of <span className="text-gradient">thought.</span>
        </h1>

        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
          Describe your app idea in plain English. Genesis AI instantly generates the UI schema, API endpoints, database architecture, and security rules.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4">
          <Link to="/dashboard">
            <AnimatedButton className="px-8 py-4 text-lg shadow-[0_0_30px_rgba(139,92,246,0.3)]">
              Start Generating
            </AnimatedButton>
          </Link>
          <Link to="/docs">
            <AnimatedButton variant="secondary" className="px-8 py-4 text-lg backdrop-blur-md">
              View Documentation
            </AnimatedButton>
          </Link>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 0.3 }}
        className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl w-full z-10 pb-20"
      >
        {[
          { icon: <Zap size={24} className="text-yellow-400" />, title: "Instant Generation", desc: "From prompt to architecture in milliseconds." },
          { icon: <Code size={24} className="text-accent-cyan" />, title: "API & Frontend Ready", desc: "Generates fully typed schemas and routes." },
          { icon: <Database size={24} className="text-accent-purple" />, title: "Smart Database Design", desc: "Normalized relational tables and auth rules automatically." },
        ].map((feature, i) => (
          <div key={i} className="glass p-8 rounded-2xl hover:bg-white/5 transition-colors border border-white/5">
            <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-6">
              {feature.icon}
            </div>
            <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
            <p className="text-gray-400">{feature.desc}</p>
          </div>
        ))}
      </motion.div>
         </div>
         <footer className="bg-dark-800 border-t border-white/10">
        <div className="container mx-auto px-4 py-8 text-center">
          <p className="text-gray-400">© 2026 Gen-Ora AI. All rights reserved.</p>
        </div>
      </footer></>
  );
};