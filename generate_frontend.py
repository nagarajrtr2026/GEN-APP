import os

base_dir = r"c:\Users\ADMIN\OneDrive\App\frontend"

files = {
    "tailwind.config.js": """
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#050816',
          800: '#0b1020',
          700: '#111827',
        },
        accent: {
          cyan: '#06b6d4',
          violet: '#8b5cf6',
          purple: '#a855f7',
        }
      },
      animation: {
        'glow-pulse': 'glow 3s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 10px #8b5cf6, 0 0 20px #8b5cf6' },
          '100%': { boxShadow: '0 0 20px #06b6d4, 0 0 40px #06b6d4' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        }
      }
    },
  },
  plugins: [],
}
    """,
    "postcss.config.js": """
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
    """,
    "src/index.css": """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-dark-900 text-white min-h-screen selection:bg-accent-violet selection:text-white overflow-x-hidden;
  }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #050816; 
}
::-webkit-scrollbar-thumb {
  background: #111827; 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #8b5cf6; 
}

/* Glassmorphism */
.glass {
  background: rgba(17, 24, 39, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.text-gradient {
  background: linear-gradient(to right, #06b6d4, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
    """,
    "src/api/client.ts": """
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});
    """,
    "src/store/useAppStore.ts": """
import { create } from 'zustand';
import { apiClient } from '../api/client';

interface AppState {
  isGenerating: boolean;
  currentResult: any;
  error: string | null;
  generateApp: (prompt: string) => Promise<void>;
  metrics: any;
  fetchMetrics: () => Promise<void>;
  history: any[];
  fetchHistory: () => Promise<void>;
}

export const useAppStore = create<AppState>((set) => ({
  isGenerating: false,
  currentResult: null,
  error: null,
  metrics: null,
  history: [],
  
  generateApp: async (prompt: string) => {
    set({ isGenerating: true, error: null });
    try {
      const res = await apiClient.post('/api/v1/generate', { prompt });
      set({ currentResult: res.data.data, isGenerating: false });
    } catch (err: any) {
      set({ error: err.response?.data?.detail || err.message, isGenerating: false });
    }
  },
  
  fetchMetrics: async () => {
    try {
      const res = await apiClient.get('/api/v1/metrics');
      set({ metrics: res.data });
    } catch (err) {
      console.error(err);
    }
  },
  
  fetchHistory: async () => {
    try {
      const res = await apiClient.get('/api/v1/history');
      set({ history: res.data });
    } catch (err) {
      console.error(err);
    }
  }
}));
    """,
    "src/components/ui/GlowCard.tsx": """
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
    """,
    "src/components/ui/AnimatedButton.tsx": """
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
    """,
    "src/components/layout/Navbar.tsx": """
import React from 'react';
import { Bot, User, Bell } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Navbar = () => {
  return (
    <nav className="h-16 border-b border-white/10 glass flex items-center justify-between px-6 sticky top-0 z-50">
      <Link to="/" className="flex items-center gap-2 group">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center shadow-[0_0_15px_rgba(139,92,246,0.5)] group-hover:shadow-[0_0_25px_rgba(6,182,212,0.8)] transition-all">
          <Bot size={20} className="text-white" />
        </div>
        <span className="text-xl font-bold tracking-wider text-gradient">GENESIS.AI</span>
      </Link>
      
      <div className="flex items-center gap-4">
        <button className="p-2 hover:bg-white/5 rounded-full transition-colors">
          <Bell size={20} className="text-gray-400 hover:text-white" />
        </button>
        <button className="w-8 h-8 rounded-full bg-gradient-to-r from-accent-purple to-accent-cyan flex items-center justify-center">
          <User size={16} className="text-white" />
        </button>
      </div>
    </nav>
  );
};
    """,
    "src/components/layout/Sidebar.tsx": """
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, History, BarChart3, Info } from 'lucide-react';
import { motion } from 'framer-motion';

export const Sidebar = () => {
  const location = useLocation();
  const links = [
    { path: '/dashboard', icon: <LayoutDashboard size={20} />, label: 'Dashboard' },
    { path: '/metrics', icon: <BarChart3 size={20} />, label: 'Metrics' },
    { path: '/history', icon: <History size={20} />, label: 'History' },
    { path: '/about', icon: <Info size={20} />, label: 'About' },
  ];

  return (
    <aside className="w-64 border-r border-white/10 glass hidden md:flex flex-col p-4 h-[calc(100vh-64px)] sticky top-16">
      <div className="flex flex-col gap-2 mt-4">
        {links.map((link) => {
          const isActive = location.pathname === link.path;
          return (
            <Link key={link.path} to={link.path} className="relative group">
              {isActive && (
                <motion.div 
                  layoutId="activeTab" 
                  className="absolute inset-0 bg-white/10 rounded-lg border border-white/5" 
                />
              )}
              <div className={`relative px-4 py-3 flex items-center gap-3 rounded-lg transition-colors ${isActive ? 'text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}>
                <span className={`${isActive ? 'text-accent-cyan' : ''}`}>{link.icon}</span>
                <span className="font-medium">{link.label}</span>
              </div>
            </Link>
          );
        })}
      </div>
      
      <div className="mt-auto p-4 rounded-xl bg-gradient-to-br from-accent-violet/20 to-transparent border border-accent-violet/20">
        <h4 className="text-sm font-bold text-white mb-2">Pro Plan</h4>
        <p className="text-xs text-gray-400 mb-3">Unlimited generations & premium support.</p>
        <button className="w-full py-2 text-xs font-bold bg-accent-violet rounded-lg hover:bg-accent-cyan transition-colors">
          Upgrade Now
        </button>
      </div>
    </aside>
  );
};
    """,
    "src/pages/LandingPage.tsx": """
import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { AnimatedButton } from '../components/ui/AnimatedButton';
import { Zap, Code, Database, Sparkles } from 'lucide-react';

export const LandingPage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center pt-32 px-4 relative overflow-hidden">
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
          <span className="text-sm text-gray-300">Genesis API v2.0 is live</span>
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
          <AnimatedButton variant="secondary" className="px-8 py-4 text-lg backdrop-blur-md">
            View Documentation
          </AnimatedButton>
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
  );
};
    """,
    "src/pages/DashboardPage.tsx": """
import React, { useState } from 'react';
import { useAppStore } from '../store/useAppStore';
import { motion, AnimatePresence } from 'framer-motion';
import { GlowCard } from '../components/ui/GlowCard';
import { Send, Copy, Database, LayoutTemplate, ShieldCheck } from 'lucide-react';

export const DashboardPage = () => {
  const [prompt, setPrompt] = useState('');
  const { generateApp, isGenerating, currentResult, error } = useAppStore();

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      generateApp(prompt);
    }
  };

  const handleCopy = () => {
    if (currentResult) {
      navigator.clipboard.writeText(JSON.stringify(currentResult, null, 2));
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto w-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Workspace</h1>
        <p className="text-gray-400">Describe your application and let AI build the architecture.</p>
      </div>

      <form onSubmit={handleGenerate} className="mb-10 relative">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="E.g., Build a CRM for real estate agents with properties, clients, appointments, and a dashboard..."
          className="w-full h-32 bg-dark-800 border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:border-accent-violet focus:ring-1 focus:ring-accent-violet transition-all resize-none glass"
        />
        <div className="absolute bottom-4 right-4 flex gap-2">
          <button 
            type="submit" 
            disabled={isGenerating || !prompt.trim()}
            className="bg-accent-violet hover:bg-accent-cyan text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            {isGenerating ? (
              <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> Generating...</>
            ) : (
              <><Send size={16} /> Generate Architecture</>
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="mb-8 p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg">
          Error: {error}
        </div>
      )}

      <AnimatePresence>
        {currentResult && !isGenerating && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-6"
          >
            <div className="lg:col-span-2 space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gradient">{currentResult.app_name || 'Generated App'}</h2>
                <span className="px-3 py-1 bg-white/5 border border-white/10 rounded-full text-xs text-accent-cyan">
                  {currentResult.app_type || 'Custom App'}
                </span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <GlowCard>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-accent-cyan/10 rounded-lg text-accent-cyan"><LayoutTemplate size={20} /></div>
                    <h3 className="text-lg font-semibold">UI Schema</h3>
                  </div>
                  <ul className="list-disc list-inside text-gray-400 text-sm">
                    {currentResult.ui_schema?.pages?.map((p: string, i: number) => <li key={i}>{p}</li>) || <li>No pages defined</li>}
                  </ul>
                </GlowCard>

                <GlowCard>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-accent-violet/10 rounded-lg text-accent-violet"><Database size={20} /></div>
                    <h3 className="text-lg font-semibold">API Endpoints</h3>
                  </div>
                  <ul className="list-disc list-inside text-gray-400 text-sm">
                    {currentResult.api_schema?.endpoints?.map((e: string, i: number) => <li key={i}>{e}</li>) || <li>No endpoints defined</li>}
                  </ul>
                </GlowCard>

                <GlowCard>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-green-500/10 rounded-lg text-green-400"><Database size={20} /></div>
                    <h3 className="text-lg font-semibold">Database Schema</h3>
                  </div>
                  <ul className="list-disc list-inside text-gray-400 text-sm">
                    {currentResult.db_schema?.tables?.map((t: string, i: number) => <li key={i}>{t}</li>) || <li>No tables defined</li>}
                  </ul>
                </GlowCard>

                <GlowCard>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-yellow-500/10 rounded-lg text-yellow-400"><ShieldCheck size={20} /></div>
                    <h3 className="text-lg font-semibold">Auth & Roles</h3>
                  </div>
                  <ul className="list-disc list-inside text-gray-400 text-sm">
                    {currentResult.auth_schema?.roles?.map((r: string, i: number) => <li key={i}>{r}</li>) || <li>No roles defined</li>}
                  </ul>
                </GlowCard>
              </div>
            </div>

            <div className="lg:col-span-1">
              <GlowCard className="h-full">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">Raw JSON Output</h3>
                  <div className="flex gap-2">
                    <button onClick={handleCopy} className="p-1.5 hover:bg-white/10 rounded text-gray-400 hover:text-white transition-colors" title="Copy JSON">
                      <Copy size={16} />
                    </button>
                  </div>
                </div>
                <div className="bg-[#050816] rounded-lg p-4 overflow-auto max-h-[600px] border border-white/5">
                  <pre className="text-xs text-accent-cyan font-mono whitespace-pre-wrap">
                    {JSON.stringify(currentResult, null, 2)}
                  </pre>
                </div>
              </GlowCard>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
    """,
    "src/pages/MetricsPage.tsx": """
import React, { useEffect } from 'react';
import { useAppStore } from '../store/useAppStore';
import { GlowCard } from '../components/ui/GlowCard';
import { Activity, CheckCircle, XCircle, Clock } from 'lucide-react';

export const MetricsPage = () => {
  const { metrics, fetchMetrics } = useAppStore();

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!metrics) return <div className="p-6 text-gray-400">Loading metrics...</div>;

  return (
    <div className="p-6 max-w-6xl mx-auto w-full">
      <h1 className="text-3xl font-bold mb-8">System Metrics</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Total Requests</p>
              <h3 className="text-3xl font-bold text-white mt-1">{metrics.total_requests}</h3>
            </div>
            <div className="p-3 bg-blue-500/10 rounded-xl text-blue-400"><Activity size={24} /></div>
          </div>
        </GlowCard>

        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Success Rate</p>
              <h3 className="text-3xl font-bold text-green-400 mt-1">
                {metrics.total_requests ? Math.round((metrics.success_requests / metrics.total_requests) * 100) : 0}%
              </h3>
            </div>
            <div className="p-3 bg-green-500/10 rounded-xl text-green-400"><CheckCircle size={24} /></div>
          </div>
        </GlowCard>

        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Failed Requests</p>
              <h3 className="text-3xl font-bold text-red-400 mt-1">{metrics.failed_requests}</h3>
            </div>
            <div className="p-3 bg-red-500/10 rounded-xl text-red-400"><XCircle size={24} /></div>
          </div>
        </GlowCard>

        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Avg Latency</p>
              <h3 className="text-3xl font-bold text-yellow-400 mt-1">{metrics.avg_latency?.toFixed(0) || 0} ms</h3>
            </div>
            <div className="p-3 bg-yellow-500/10 rounded-xl text-yellow-400"><Clock size={24} /></div>
          </div>
        </GlowCard>
      </div>
      
      {/* Chart Placeholders */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlowCard className="h-80 flex flex-col items-center justify-center border border-white/5">
          <p className="text-gray-500 font-mono">Performance Chart (Recharts integration placeholder)</p>
        </GlowCard>
        <GlowCard className="h-80 flex flex-col items-center justify-center border border-white/5">
          <p className="text-gray-500 font-mono">Usage Distribution (Recharts integration placeholder)</p>
        </GlowCard>
      </div>
    </div>
  );
};
    """,
    "src/pages/HistoryPage.tsx": """
import React, { useEffect } from 'react';
import { useAppStore } from '../store/useAppStore';
import { GlowCard } from '../components/ui/GlowCard';

export const HistoryPage = () => {
  const { history, fetchHistory } = useAppStore();

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto w-full">
      <h1 className="text-3xl font-bold mb-8">Generation History</h1>
      
      <div className="space-y-4">
        {history.length === 0 ? (
          <p className="text-gray-400">No history found.</p>
        ) : (
          history.map((item: any, i: number) => (
            <GlowCard key={i} className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-gray-500">{new Date(item.created_at).toLocaleString()}</span>
                <span className={`text-xs px-2 py-1 rounded-full ${item.success ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                  {item.success ? 'Success' : 'Failed'}
                </span>
              </div>
              <p className="text-white font-medium mb-3">"{item.prompt}"</p>
              <div className="flex gap-4 text-xs text-gray-400">
                <span>Provider: {item.provider}</span>
                <span>Latency: {item.latency_ms?.toFixed(0) || 0} ms</span>
              </div>
            </GlowCard>
          ))
        )}
      </div>
    </div>
  );
};
    """,
    "src/pages/AboutPage.tsx": """
import React from 'react';

export const AboutPage = () => {
  return (
    <div className="p-6 max-w-4xl mx-auto w-full">
      <h1 className="text-4xl font-bold mb-6 text-gradient">Genesis Architecture AI</h1>
      <div className="glass p-8 rounded-2xl border border-white/5 space-y-6 text-gray-300 leading-relaxed">
        <p>
          Genesis AI represents the next generation of software compilation. Instead of writing code manually, you declare your intent, and our proprietary pipeline translates your natural language into fully structured, production-ready system architectures.
        </p>
        <p>
          Powered by advanced language models and deterministic validation engines, Genesis bridges the gap between idea and execution in milliseconds.
        </p>
        <div className="mt-8 pt-8 border-t border-white/10">
          <h3 className="text-xl font-bold text-white mb-4">Core Technology Stack</h3>
          <ul className="list-disc list-inside space-y-2 text-gray-400">
            <li>React 18 + Vite Frontend</li>
            <li>Zustand State Management</li>
            <li>Framer Motion Animations</li>
            <li>FastAPI + Python 3.11 Backend</li>
            <li>SQLAlchemy ORM + SQLite</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
    """,
    "src/App.tsx": """
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { MetricsPage } from './pages/MetricsPage';
import { HistoryPage } from './pages/HistoryPage';
import { AboutPage } from './pages/AboutPage';

const PageWrapper = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();
  const isLanding = location.pathname === '/';

  if (isLanding) {
    return <>{children}</>;
  }

  return (
    <div className="flex flex-col h-screen">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto relative">
          <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.02] pointer-events-none mix-blend-overlay" />
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
            className="h-full"
          >
            {children}
          </motion.div>
        </main>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <PageWrapper>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/metrics" element={<MetricsPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </PageWrapper>
    </Router>
  );
}

export default App;
    """,
    "src/main.tsx": """
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
    """
}

# Create all files on disk
for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
        
print(f"Frontend files successfully generated at {base_dir}")
