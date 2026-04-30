import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '../store/useAppStore';
import { motion, AnimatePresence } from 'framer-motion';
import { GlowCard } from '../components/ui/GlowCard';
import { Send, Copy, Database, LayoutTemplate, ShieldCheck, Monitor, Briefcase } from 'lucide-react';

export const DashboardPage = () => {
  const [prompt, setPrompt] = useState('');
  const { generateApp, isGenerating, currentResult, error } = useAppStore();
  const navigate = useNavigate();

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
                <div className="flex items-center gap-4">
                  <h2 className="text-2xl font-bold text-gradient">{currentResult.app_name || 'Generated App'}</h2>
                  <span className="px-3 py-1 bg-white/5 border border-white/10 rounded-full text-xs text-accent-cyan">
                    {currentResult.app_type || 'Custom App'}
                  </span>
                </div>
                <button
                  onClick={() => navigate('/preview')}
                  className="bg-accent-cyan/10 border border-accent-cyan/30 text-accent-cyan hover:bg-accent-cyan hover:text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
                >
                  <Monitor size={16} /> Live Preview
                </button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <GlowCard>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-accent-cyan/10 rounded-lg text-accent-cyan"><LayoutTemplate size={20} /></div>
                    <h3 className="text-lg font-semibold">UI Schema</h3>
                  </div>
                  <div className="text-gray-400 text-sm mb-2">Total Pages: {currentResult.ui?.pages?.length || 0}</div>
                  <ul className="list-disc list-inside text-gray-400 text-sm mb-2">
                    {currentResult.ui?.pages?.map((p: any, i: number) => (
                      <li key={i}>{typeof p === 'string' ? p : `${p.name} (${p.components?.length || 0} components)`}</li>
                    )) || <li>No pages defined</li>}
                  </ul>
                  {currentResult.ui?.layout?.type && (
                    <div className="text-xs px-2 py-1 bg-white/5 inline-block rounded border border-white/10 text-gray-300">
                      Layout: {currentResult.ui.layout.type}
                    </div>
                  )}
                </GlowCard>

                <GlowCard>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-accent-violet/10 rounded-lg text-accent-violet"><Database size={20} /></div>
                    <h3 className="text-lg font-semibold">API Endpoints</h3>
                  </div>
                  <div className="text-gray-400 text-sm mb-2">Total Endpoints: {currentResult.api?.endpoints?.length || 0}</div>
                  <ul className="list-disc list-inside text-gray-400 text-sm">
                    {currentResult.api?.endpoints?.map((e: any, i: number) => (
                      <li key={i}>{typeof e === 'string' ? e : <><span className="text-accent-cyan font-mono text-xs mr-1">{e.method}</span>{e.path}</>}</li>
                    )) || <li>No endpoints defined</li>}
                  </ul>
                </GlowCard>

                <GlowCard>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-green-500/10 rounded-lg text-green-400"><Database size={20} /></div>
                    <h3 className="text-lg font-semibold">Database Schema</h3>
                  </div>
                  <div className="text-gray-400 text-sm mb-2">Total Tables: {currentResult.database?.tables?.length || 0}</div>
                  <ul className="list-disc list-inside text-gray-400 text-sm">
                    {currentResult.database?.tables?.map((t: any, i: number) => (
                      <li key={i}>{typeof t === 'string' ? t : `${t.name} (${t.columns?.length || 0} cols)`}</li>
                    )) || <li>No tables defined</li>}
                  </ul>
                </GlowCard>

                <GlowCard>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-yellow-500/10 rounded-lg text-yellow-400"><ShieldCheck size={20} /></div>
                    <h3 className="text-lg font-semibold">Auth & Roles</h3>
                  </div>
                  <ul className="list-disc list-inside text-gray-400 text-sm mb-3">
                    {currentResult.auth?.roles?.map((r: string, i: number) => (
                      <li key={i} className="capitalize">{r}</li>
                    )) || <li>No roles defined</li>}
                  </ul>
                  {currentResult.auth?.permissions && (
                    <div className="flex flex-wrap gap-2">
                      {Object.keys(currentResult.auth.permissions).map((role, i) => (
                        <span key={i} className="text-[10px] px-2 py-0.5 rounded-full bg-yellow-500/20 text-yellow-300 border border-yellow-500/30">
                          {role}
                        </span>
                      ))}
                    </div>
                  )}
                </GlowCard>

                {currentResult.business_logic && currentResult.business_logic.length > 0 && (
                  <GlowCard className="md:col-span-2">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400"><Briefcase size={20} /></div>
                      <h3 className="text-lg font-semibold">Business Logic</h3>
                    </div>
                    <ul className="list-disc list-inside text-gray-400 text-sm">
                      {currentResult.business_logic.map((logic: string, i: number) => (
                        <li key={i}>{logic}</li>
                      ))}
                    </ul>
                  </GlowCard>
                )}
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
