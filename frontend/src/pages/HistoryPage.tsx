import{ useEffect } from 'react';
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
