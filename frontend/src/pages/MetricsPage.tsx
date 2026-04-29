import React, { useEffect } from 'react';
import { useAppStore } from '../store/useAppStore';
import { GlowCard } from '../components/ui/GlowCard';
import { Activity, CheckCircle, XCircle, Clock } from 'lucide-react';

export const MetricsPage = () => {
  const { metrics, fetchMetrics } = useAppStore();

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!metrics) return <div className="p-6 text-gray-400">Loading metrics...</div>;

  return (
    <div className="p-6 max-w-6xl mx-auto w-full">
      <h1 className="text-3xl font-bold mb-8">System Metrics</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Total Requests</p>
              <h3 className="text-3xl font-bold text-white mt-1">{metrics.total_requests}</h3>
            </div>
            <div className="p-3 bg-blue-500/10 rounded-xl text-blue-400"><Activity size={24} /></div>
          </div>
        </GlowCard>

        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Success Rate</p>
              <h3 className="text-3xl font-bold text-green-400 mt-1">
                {metrics.total_requests ? Math.round((metrics.success_requests / metrics.total_requests) * 100) : 0}%
              </h3>
            </div>
            <div className="p-3 bg-green-500/10 rounded-xl text-green-400"><CheckCircle size={24} /></div>
          </div>
        </GlowCard>

        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Failed Requests</p>
              <h3 className="text-3xl font-bold text-red-400 mt-1">{metrics.failed_requests}</h3>
            </div>
            <div className="p-3 bg-red-500/10 rounded-xl text-red-400"><XCircle size={24} /></div>
          </div>
        </GlowCard>

        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Avg Latency</p>
              <h3 className="text-3xl font-bold text-yellow-400 mt-1">{metrics.avg_latency?.toFixed(0) || 0} ms</h3>
            </div>
            <div className="p-3 bg-yellow-500/10 rounded-xl text-yellow-400"><Clock size={24} /></div>
          </div>
        </GlowCard>
      </div>
      
      {/* Chart Placeholders */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlowCard className="h-80 flex flex-col items-center justify-center border border-white/5">
          <p className="text-gray-500 font-mono">Performance Chart (Recharts integration placeholder)</p>
        </GlowCard>
        <GlowCard className="h-80 flex flex-col items-center justify-center border border-white/5">
          <p className="text-gray-500 font-mono">Usage Distribution (Recharts integration placeholder)</p>
        </GlowCard>
      </div>
    </div>
  );
};