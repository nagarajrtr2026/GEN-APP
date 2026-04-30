import { Bot, User, Bell } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Navbar = () => {
  return (
    <nav className="h-16 border-b border-white/10 glass flex items-center justify-between px-6 sticky top-0 z-50">
      <Link to="/" className="flex items-center gap-2 group">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center shadow-[0_0_15px_rgba(139,92,246,0.5)] group-hover:shadow-[0_0_25px_rgba(6,182,212,0.8)] transition-all">
          <Bot size={20} className="text-white" />
        </div>
        <span className="text-xl font-bold tracking-wider text-gradient">Gen-Ora AI</span>
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