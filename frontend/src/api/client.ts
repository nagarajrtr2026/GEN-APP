import axios from 'axios';

export const apiClient = axios.create({
  baseURL: 'https://gen-app-u1l1.onrender.com',
  headers: {
    'Content-Type': 'application/json',
  },
});
