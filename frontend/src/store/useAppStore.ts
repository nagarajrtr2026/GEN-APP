import { create } from 'zustand';
import { apiClient } from '../api/client';

interface AppState {
  isGenerating: boolean;
  currentResult: any;
  error: string | null;
  generateApp: (prompt: string) => Promise<void>;
  metrics: any;
  fetchMetrics: () => Promise<void>;
  history: any[];
  fetchHistory: () => Promise<void>;
}

export const useAppStore = create<AppState>((set) => ({
  isGenerating: false,
  currentResult: null,
  error: null,
  metrics: null,
  history: [],
  
  generateApp: async (prompt: string) => {
    set({ isGenerating: true, error: null });
    try {
      const res = await apiClient.post('/api/v1/generate', { prompt });
      set({ currentResult: res.data.data, isGenerating: false });
    } catch (err: any) {
      set({ error: err.response?.data?.detail || err.message, isGenerating: false });
    }
  },
  
  fetchMetrics: async () => {
    try {
      const res = await apiClient.get('/api/v1/metrics');
      set({ metrics: res.data });
    } catch (err) {
      console.error(err);
    }
  },
  
  fetchHistory: async () => {
    try {
      const res = await apiClient.get('/api/v1/history');
      set({ history: res.data });
    } catch (err) {
      console.error(err);
    }
  }
}));