import React from 'react';

export const AboutPage = () => {
  return (
    <div className="p-6 max-w-4xl mx-auto w-full">
      <h1 className="text-4xl font-bold mb-6 text-gradient">Gen-Ora Architecture AI</h1>
      <div className="glass p-8 rounded-2xl border border-white/5 space-y-6 text-gray-300 leading-relaxed">
        <p>
          Gen-Ora AI represents the next generation of software compilation. Instead of writing code manually, you declare your intent, and our proprietary pipeline translates your natural language into fully structured, production-ready system architectures.
        </p>
        <p>
          Powered by advanced language models and deterministic validation engines, Gen-Ora AI bridges the gap between idea and execution in milliseconds.
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