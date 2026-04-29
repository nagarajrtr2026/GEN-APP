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