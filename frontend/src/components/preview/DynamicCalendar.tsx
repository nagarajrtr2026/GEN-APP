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