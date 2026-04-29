import React from 'react';
import { Users, DollarSign, TrendingUp, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

export const DynamicCards = ({ pageName }: { pageName: string }) => {
  const isEcommerce = pageName.toLowerCase().includes('product') || pageName.toLowerCase().includes('order');
  
  const stats = [
    { title: isEcommerce ? 'Total Revenue' : 'Total Users', value: isEcommerce ? '$45,231' : '12,345', icon: isEcommerce ? <DollarSign size={20} /> : <Users size={20} />, color: 'text-accent-cyan' },
    { title: 'Active Now', value: '+573', icon: <Activity size={20} />, color: 'text-green-400' },
    { title: 'Growth Rate', value: '+24.5%', icon: <TrendingUp size={20} />, color: 'text-accent-violet' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {stats.map((stat, i) => (
        <motion.div 
          key={i}
          whileHover={{ y: -5 }}
          className="p-6 rounded-2xl bg-dark-800 border border-white/5 shadow-lg relative overflow-hidden group"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full blur-3xl group-hover:bg-accent-cyan/10 transition-colors" />
          <div className="flex justify-between items-start mb-4 relative z-10">
            <span className="text-gray-400 font-medium">{stat.title}</span>
            <div className={`p-2 rounded-lg bg-white/5 ${stat.color}`}>{stat.icon}</div>
          </div>
          <h3 className="text-3xl font-bold relative z-10">{stat.value}</h3>
        </motion.div>
      ))}
    </div>
  );
};