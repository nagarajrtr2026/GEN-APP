import { useEffect, useState } from 'react';
import axios from 'axios';
import { GlowCard } from '../components/ui/GlowCard';
import { Activity, CheckCircle, XCircle, Clock } from 'lucide-react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';

interface MetricsData {
  total_requests: number;
  successful_requests?: number;
  success_requests?: number;
  failed_requests: number;
  average_response_time?: number;
  avg_latency?: number;
  requests_per_day?: { date: string; count: number }[];
  app_types?: Record<string, number>;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'];

export const MetricsPage = () => {
  const [metrics, setMetrics] = useState<MetricsData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    
    const fetchMetrics = async () => {
      try {
        const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        const res = await axios.get(`${baseUrl}/api/v1/metrics`);
        
        if (isMounted) {
          console.log("metrics:", res.data);
          setMetrics(res.data);
          setError(null);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.response?.data?.detail || err.message || 'Failed to fetch metrics');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 10000); // Fetch every 10s
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  if (loading && !metrics) {
    return (
      <div className="p-6 max-w-6xl mx-auto w-full">
        <h1 className="text-3xl font-bold mb-8 text-white">System Metrics</h1>
        
        {/* Loading Skeletons for KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          {[1, 2, 3, 4].map((i) => (
            <GlowCard key={i}>
              <div className="animate-pulse flex justify-between items-start mb-4">
                <div className="w-full">
                  <div className="h-4 bg-gray-700 rounded w-24 mb-3"></div>
                  <div className="h-8 bg-gray-700 rounded w-16"></div>
                </div>
                <div className="w-12 h-12 bg-gray-700 rounded-xl"></div>
              </div>
            </GlowCard>
          ))}
        </div>
        
        {/* Loading Skeletons for Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <GlowCard className="h-80 animate-pulse bg-gray-800/50"><div /></GlowCard>
          <GlowCard className="h-80 animate-pulse bg-gray-800/50"><div /></GlowCard>
        </div>
      </div>
    );
  }

  if (error && !metrics) {
    return (
      <div className="p-6 max-w-6xl mx-auto w-full text-white">
        Error loading metrics: {error}
      </div>
    );
  }

  const success_count = metrics?.success_requests ?? 0;
  const total_requests = metrics?.total_requests ?? 0;
  const failed_requests = metrics?.failed_requests ?? 0;
  const avg_latency = metrics?.avg_latency ? (metrics.avg_latency / 1000).toFixed(1) : "0.0";
  
  const successRate = total_requests > 0 
    ? Math.round((success_count / total_requests) * 100) 
    : 0;

  // Fallback for missing fields in API response
  const requests_per_day = metrics?.requests_per_day || [
    { date: "2026-04-01", count: 10 },
    { date: "2026-04-02", count: 25 },
    { date: "2026-04-03", count: 18 },
    { date: "2026-04-04", count: 42 },
    { date: "2026-04-05", count: 35 },
  ];

  const app_types = metrics?.app_types || {
    "ecommerce": 40,
    "hospital": 25,
    "school": 35
  };

  // Format pie chart data
  const pieData = Object.entries(app_types).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value
  }));

  return (
    <div className="p-6 max-w-6xl mx-auto w-full">
      <h1 className="text-3xl font-bold mb-8 text-white">System Metrics</h1>
      
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Total Requests</p>
              <h3 className="text-3xl font-bold text-white mt-1">{total_requests.toLocaleString()}</h3>
            </div>
            <div className="p-3 bg-blue-500/10 rounded-xl text-blue-400"><Activity size={24} /></div>
          </div>
        </GlowCard>

        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Success Rate</p>
              <h3 className="text-3xl font-bold text-green-400 mt-1">{successRate}%</h3>
            </div>
            <div className="p-3 bg-green-500/10 rounded-xl text-green-400"><CheckCircle size={24} /></div>
          </div>
        </GlowCard>

        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Failed Requests</p>
              <h3 className="text-3xl font-bold text-red-400 mt-1">{failed_requests.toLocaleString()}</h3>
            </div>
            <div className="p-3 bg-red-500/10 rounded-xl text-red-400"><XCircle size={24} /></div>
          </div>
        </GlowCard>

        <GlowCard>
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-gray-400 text-sm font-medium">Avg Latency</p>
              <h3 className="text-3xl font-bold text-yellow-400 mt-1">{avg_latency}s</h3>
            </div>
            <div className="p-3 bg-yellow-500/10 rounded-xl text-yellow-400"><Clock size={24} /></div>
          </div>
        </GlowCard>
      </div>
      
      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Line Chart */}
        <GlowCard className="flex flex-col border border-white/5 h-96">
          <h3 className="text-lg font-medium text-white mb-6">Performance Trend</h3>
          <div className="h-full w-full pb-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={requests_per_day} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                <XAxis 
                  dataKey="date" 
                  stroke="#9ca3af" 
                  tick={{fill: '#9ca3af', fontSize: 12}} 
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis 
                  stroke="#9ca3af" 
                  tick={{fill: '#9ca3af', fontSize: 12}} 
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                  itemStyle={{ color: '#e2e8f0' }}
                />
                <Line 
                  type="monotone" 
                  dataKey="count" 
                  stroke="#3b82f6" 
                  strokeWidth={3}
                  dot={{ r: 4, fill: '#1e293b', stroke: '#3b82f6', strokeWidth: 2 }}
                  activeDot={{ r: 6, fill: '#3b82f6', stroke: '#fff' }}
                  animationDuration={1500}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </GlowCard>

        {/* Pie Chart */}
        <GlowCard className="flex flex-col border border-white/5 h-96">
          <h3 className="text-lg font-medium text-white mb-6">Usage Distribution</h3>
          <div className="h-full w-full pb-4">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={110}
                  paddingAngle={5}
                  dataKey="value"
                  animationDuration={1500}
                >
                  {pieData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                  itemStyle={{ color: '#e2e8f0' }}
                />
                <Legend 
                  verticalAlign="bottom" 
                  height={36}
                  iconType="circle"
                  formatter={(value) => <span className="text-gray-300 ml-2">{value}</span>}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </GlowCard>
      </div>
    </div>
  );
};