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