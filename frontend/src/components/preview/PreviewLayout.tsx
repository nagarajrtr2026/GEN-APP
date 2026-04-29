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