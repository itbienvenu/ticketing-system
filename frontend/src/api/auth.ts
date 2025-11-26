import axios from 'axios';
import type { RegisterUser, LoginUser, UserOut  } from '../types/user';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

export const registerUser = async (data: RegisterUser): Promise<UserOut> => {
  const response = await axios.post(`${API_BASE}/register`, data);
  return response.data;
};

export const loginUser = async (data: LoginUser): Promise<{ access_token: string; user: UserOut }> => {
  const response = await axios.post(`${API_BASE}/login`, data);
  return response.data;
};

export const getMe = async (token: string): Promise<UserOut> => {
  const response = await axios.get(`${API_BASE}/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};
