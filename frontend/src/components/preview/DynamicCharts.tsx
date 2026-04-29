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