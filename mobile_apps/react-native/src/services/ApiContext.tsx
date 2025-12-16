import React, { createContext, useContext } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5555';

interface ApiContextType {
  get: (endpoint: string) => Promise<any>;
  post: (endpoint: string, data: any) => Promise<any>;
}

const ApiContext = createContext<ApiContextType | undefined>(undefined);

export const ApiProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
  });

  const get = async (endpoint: string) => {
    const response = await api.get(endpoint);
    return response.data;
  };

  const post = async (endpoint: string, data: any) => {
    const response = await api.post(endpoint, data);
    return response.data;
  };

  return (
    <ApiContext.Provider value={{ get, post }}>
      {children}
    </ApiContext.Provider>
  );
};

export const useApi = () => {
  const context = useContext(ApiContext);
  if (!context) {
    throw new Error('useApi must be used within ApiProvider');
  }
  return context;
};
