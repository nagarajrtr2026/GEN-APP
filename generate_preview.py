import os

base_dir = r"c:\Users\ADMIN\OneDrive\App\frontend\src\components\preview"
os.makedirs(base_dir, exist_ok=True)

files = {
    "PreviewLayout.tsx": """
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppStore } from '../../store/useAppStore';
import { EmptyPreviewState } from './EmptyPreviewState';
import { DynamicRenderer } from './DynamicRenderer';
import { motion, AnimatePresence } from 'framer-motion';
import { Monitor, Smartphone, Tablet, ChevronLeft, Moon, Sun } from 'lucide-react';

export const PreviewLayout = () => {
  const { currentResult } = useAppStore();
  const { pageName } = useParams();
  const navigate = useNavigate();
  const [device, setDevice] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  if (!currentResult) {
    return <EmptyPreviewState />;
  }

  // Parse pages safely
  let pages: any[] = [];
  if (currentResult.ui_schema?.pages) {
    const rawPages = currentResult.ui_schema.pages;
    pages = rawPages.map((p: any) => {
      if (typeof p === 'string') {
        const lower = p.toLowerCase();
        let comps = ['form', 'table'];
        if (lower.includes('dashboard')) comps = ['cards', 'charts', 'table'];
        if (lower.includes('calendar') || lower.includes('appointment')) comps = ['calendar'];
        if (lower.includes('login') || lower.includes('register')) comps = ['form'];
        return { name: p, components: comps };
      }
      return p;
    });
  } else if (currentResult.ui?.pages) {
      pages = currentResult.ui.pages;
  }

  const activePage = pageName 
    ? pages.find(p => p.name.toLowerCase() === pageName.toLowerCase()) 
    : pages[0];

  const deviceStyles = {
    desktop: "w-full h-full",
    tablet: "w-[768px] h-[1024px] mx-auto border-8 border-dark-800 rounded-[2rem] shadow-2xl overflow-hidden mt-8",
    mobile: "w-[375px] h-[812px] mx-auto border-[12px] border-dark-800 rounded-[3rem] shadow-2xl overflow-hidden mt-8"
  };

  return (
    <div className="flex flex-col h-screen bg-dark-900 text-white overflow-hidden">
      {/* Top Navbar */}
      <div className="h-14 border-b border-white/10 flex items-center justify-between px-4 glass z-50">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/dashboard')} className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
            <ChevronLeft size={18} /> Back to Dashboard
          </button>
          <div className="h-4 w-px bg-white/20" />
          <h2 className="font-bold text-gradient">{currentResult.app_name || 'Generated Preview'}</h2>
        </div>
        
        <div className="flex items-center gap-2 bg-dark-800 p-1 rounded-lg border border-white/5">
          <button onClick={() => setDevice('desktop')} className={`p-1.5 rounded-md transition-colors ${device === 'desktop' ? 'bg-white/10 text-accent-cyan' : 'text-gray-400 hover:text-white'}`}><Monitor size={16} /></button>
          <button onClick={() => setDevice('tablet')} className={`p-1.5 rounded-md transition-colors ${device === 'tablet' ? 'bg-white/10 text-accent-cyan' : 'text-gray-400 hover:text-white'}`}><Tablet size={16} /></button>
          <button onClick={() => setDevice('mobile')} className={`p-1.5 rounded-md transition-colors ${device === 'mobile' ? 'bg-white/10 text-accent-cyan' : 'text-gray-400 hover:text-white'}`}><Smartphone size={16} /></button>
        </div>
        
        <div className="flex items-center gap-2">
           <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} className="p-2 hover:bg-white/5 rounded-full text-gray-400 hover:text-white">
             {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
           </button>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden relative bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-blend-overlay">
        {/* Sidebar */}
        <div className="w-64 border-r border-white/10 glass flex flex-col pt-4 z-40 hidden md:flex">
          <div className="px-4 pb-2 text-xs font-bold text-gray-500 uppercase tracking-wider">Pages</div>
          <div className="flex-1 overflow-y-auto">
            {pages.map((p, i) => {
              const isActive = activePage?.name === p.name;
              return (
                <button
                  key={i}
                  onClick={() => navigate(`/preview/${p.name.toLowerCase()}`)}
                  className={`w-full text-left px-6 py-3 relative group transition-colors ${isActive ? 'text-white font-medium' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
                >
                  {isActive && <motion.div layoutId="preview-active" className="absolute left-0 top-0 w-1 h-full bg-accent-cyan" />}
                  {p.name}
                </button>
              );
            })}
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden p-4 relative">
          <div className={`transition-all duration-500 bg-dark-900 relative ${deviceStyles[device]} ${theme === 'light' ? '!bg-gray-50 !text-black' : ''}`}>
             <AnimatePresence mode="wait">
               <motion.div
                 key={activePage?.name || 'empty'}
                 initial={{ opacity: 0, scale: 0.98 }}
                 animate={{ opacity: 1, scale: 1 }}
                 exit={{ opacity: 0 }}
                 transition={{ duration: 0.4 }}
                 className="h-full w-full p-6 overflow-y-auto"
               >
                 <div className="max-w-6xl mx-auto space-y-8">
                    <h1 className="text-3xl font-bold mb-6 border-b border-white/10 pb-4">{activePage?.name || 'Home'}</h1>
                    {activePage?.components && activePage.components.length > 0 ? (
                      <DynamicRenderer components={activePage.components} pageName={activePage.name} />
                    ) : (
                      <div className="p-8 text-center border border-dashed border-white/20 rounded-xl text-gray-500">
                        No components defined for this page.
                      </div>
                    )}
                 </div>
               </motion.div>
             </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
};
    """,
    "EmptyPreviewState.tsx": """
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
    """,
    "DynamicRenderer.tsx": """
import React from 'react';
import { DynamicTable } from './DynamicTable';
import { DynamicForm } from './DynamicForm';
import { DynamicCards } from './DynamicCards';
import { DynamicCharts } from './DynamicCharts';
import { DynamicCalendar } from './DynamicCalendar';

interface Props {
  components: string[];
  pageName: string;
}

export const DynamicRenderer: React.FC<Props> = ({ components, pageName }) => {
  return (
    <div className="space-y-8">
      {components.map((comp, idx) => {
        const type = comp.toLowerCase();
        if (type === 'cards') return <DynamicCards key={idx} pageName={pageName} />;
        if (type === 'charts') return <DynamicCharts key={idx} pageName={pageName} />;
        if (type === 'table') return <DynamicTable key={idx} pageName={pageName} />;
        if (type === 'form') return <DynamicForm key={idx} pageName={pageName} />;
        if (type === 'calendar') return <DynamicCalendar key={idx} />;
        
        return (
          <div key={idx} className="p-6 rounded-xl bg-white/5 border border-white/10 text-center text-gray-400">
            Unknown Component: {comp}
          </div>
        );
      })}
    </div>
  );
};
    """,
    "DynamicCards.tsx": """
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
    """,
    "DynamicCharts.tsx": """
import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const data = [
  { name: 'Jan', value: 4000, secondary: 2400 },
  { name: 'Feb', value: 3000, secondary: 1398 },
  { name: 'Mar', value: 2000, secondary: 9800 },
  { name: 'Apr', value: 2780, secondary: 3908 },
  { name: 'May', value: 1890, secondary: 4800 },
  { name: 'Jun', value: 2390, secondary: 3800 },
  { name: 'Jul', value: 3490, secondary: 4300 },
];

export const DynamicCharts = ({ pageName }: { pageName: string }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="h-80 p-6 rounded-2xl bg-dark-800 border border-white/5 shadow-lg">
        <h3 className="text-lg font-bold mb-6">Trends Overview</h3>
        <ResponsiveContainer width="100%" height="80%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
            <XAxis dataKey="name" stroke="#ffffff50" axisLine={false} tickLine={false} />
            <YAxis stroke="#ffffff50" axisLine={false} tickLine={false} />
            <Tooltip contentStyle={{ backgroundColor: '#0b1020', borderColor: '#ffffff20', borderRadius: '8px' }} />
            <Area type="monotone" dataKey="value" stroke="#06b6d4" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="h-80 p-6 rounded-2xl bg-dark-800 border border-white/5 shadow-lg">
        <h3 className="text-lg font-bold mb-6">Distribution</h3>
        <ResponsiveContainer width="100%" height="80%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
            <XAxis dataKey="name" stroke="#ffffff50" axisLine={false} tickLine={false} />
            <Tooltip cursor={{ fill: '#ffffff05' }} contentStyle={{ backgroundColor: '#0b1020', borderColor: '#ffffff20', borderRadius: '8px' }} />
            <Bar dataKey="secondary" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
    """,
    "DynamicTable.tsx": """
import React from 'react';

export const DynamicTable = ({ pageName }: { pageName: string }) => {
  const lower = pageName.toLowerCase();
  let headers = ['Name', 'Email', 'Role', 'Status'];
  let rows = [
    { name: 'Alice Smith', email: 'alice@example.com', role: 'Admin', status: 'Active' },
    { name: 'Bob Jones', email: 'bob@example.com', role: 'User', status: 'Offline' },
    { name: 'Charlie Day', email: 'charlie@example.com', role: 'User', status: 'Active' },
  ];

  if (lower.includes('product')) {
    headers = ['Product Name', 'Category', 'Price', 'Stock'];
    rows = [
      { name: 'Premium Wireless Headphones', email: 'Electronics', role: '$299', status: 'In Stock' },
      { name: 'Mechanical Keyboard', email: 'Electronics', role: '$149', status: 'Low Stock' },
      { name: 'Ergonomic Chair', email: 'Furniture', role: '$499', status: 'Out of Stock' },
    ];
  } else if (lower.includes('student')) {
    headers = ['Student Name', 'Grade', 'GPA', 'Status'];
    rows = [
      { name: 'Emma Wilson', email: '10th', role: '3.8', status: 'Enrolled' },
      { name: 'Liam Garcia', email: '11th', role: '3.5', status: 'Enrolled' },
    ];
  }

  return (
    <div className="w-full bg-dark-800 border border-white/5 rounded-2xl shadow-lg overflow-hidden">
      <div className="p-6 border-b border-white/5 flex justify-between items-center">
        <h3 className="text-lg font-bold capitalize">{pageName} Data</h3>
        <div className="flex gap-2">
          <input type="text" placeholder="Search..." className="bg-dark-900 border border-white/10 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-accent-cyan text-white" />
          <button className="bg-accent-violet hover:bg-accent-cyan text-white px-4 py-1.5 rounded-lg text-sm font-medium transition-colors">Export</button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/5">
              {headers.map((h, i) => (
                <th key={i} className="p-4 text-xs font-semibold text-gray-400 uppercase tracking-wider border-b border-white/5">{h}</th>
              ))}
              <th className="p-4 text-xs font-semibold text-gray-400 uppercase tracking-wider border-b border-white/5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td className="p-4 font-medium text-white">{r.name}</td>
                <td className="p-4 text-gray-300">{r.email}</td>
                <td className="p-4 text-gray-300">{r.role}</td>
                <td className="p-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                    r.status.includes('Active') || r.status.includes('In Stock') || r.status.includes('Enrolled') 
                    ? 'bg-green-500/20 text-green-400' 
                    : r.status.includes('Low') || r.status.includes('Offline') 
                    ? 'bg-yellow-500/20 text-yellow-400'
                    : 'bg-red-500/20 text-red-400'
                  }`}>
                    {r.status}
                  </span>
                </td>
                <td className="p-4 text-right">
                  <button className="text-accent-cyan hover:text-white transition-colors text-sm font-medium">Edit</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
    """,
    "DynamicForm.tsx": """
import React from 'react';

export const DynamicForm = ({ pageName }: { pageName: string }) => {
  return (
    <div className="w-full max-w-2xl bg-dark-800 border border-white/5 rounded-2xl shadow-lg p-8">
      <h3 className="text-2xl font-bold mb-6 capitalize">Add New {pageName.replace(/s$/, '')}</h3>
      <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-400">Name</label>
            <input type="text" className="w-full bg-dark-900 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-accent-cyan focus:ring-1 focus:ring-accent-cyan transition-all" placeholder="Enter name" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-400">Primary Contact</label>
            <input type="text" className="w-full bg-dark-900 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-accent-cyan focus:ring-1 focus:ring-accent-cyan transition-all" placeholder="Email or Phone" />
          </div>
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-400">Description / Notes</label>
          <textarea rows={4} className="w-full bg-dark-900 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-accent-cyan focus:ring-1 focus:ring-accent-cyan transition-all resize-none" placeholder="Enter details..."></textarea>
        </div>
        <div className="pt-4 flex justify-end gap-4 border-t border-white/5">
          <button type="button" className="px-6 py-2 rounded-lg font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-colors">Cancel</button>
          <button type="button" className="px-6 py-2 rounded-lg font-medium bg-accent-violet hover:bg-accent-cyan text-white shadow-[0_0_15px_rgba(139,92,246,0.3)] transition-all">Save Record</button>
        </div>
      </form>
    </div>
  );
};
    """,
    "DynamicCalendar.tsx": """
import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export const DynamicCalendar = () => {
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const dates = Array.from({length: 30}, (_, i) => i + 1);

  return (
    <div className="w-full max-w-4xl bg-dark-800 border border-white/5 rounded-2xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold">November 2026</h3>
        <div className="flex gap-2">
          <button className="p-2 rounded-lg hover:bg-white/5 border border-white/10"><ChevronLeft size={18} /></button>
          <button className="p-2 rounded-lg hover:bg-white/5 border border-white/10"><ChevronRight size={18} /></button>
        </div>
      </div>
      <div className="grid grid-cols-7 gap-2 text-center mb-2">
        {days.map(d => <div key={d} className="text-xs font-bold text-gray-500 uppercase tracking-wider">{d}</div>)}
      </div>
      <div className="grid grid-cols-7 gap-2">
        {dates.map(d => (
          <div key={d} className={`aspect-square p-2 rounded-xl border ${d === 15 ? 'border-accent-cyan bg-accent-cyan/10' : 'border-white/5 hover:border-white/20 bg-dark-900'} relative cursor-pointer transition-colors flex flex-col items-start`}>
             <span className={`font-medium ${d === 15 ? 'text-accent-cyan' : 'text-gray-300'}`}>{d}</span>
             {d === 12 && <div className="mt-1 w-full text-[10px] bg-accent-violet/20 text-accent-violet rounded px-1 truncate">Meeting</div>}
             {d === 15 && <div className="mt-1 w-full text-[10px] bg-green-500/20 text-green-400 rounded px-1 truncate">Review</div>}
          </div>
        ))}
      </div>
    </div>
  );
};
    """
}

for filename, content in files.items():
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(content.strip())

print("Preview components generated successfully.")
