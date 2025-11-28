import axios from 'axios';
import axiosClient from './axiosClient';


import type { RegisterUser, LoginUser, UserOut  } from '../types/user';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

export const registerUser = async (data: RegisterUser): Promise<UserOut> => {
  const response = await axiosClient.post(`/register`, data);
  return response.data;
};

export const loginUser = async (data: LoginUser): Promise<{ access_token: string; user: UserOut }> => {
  const response = await axiosClient.post(`/login`, data);
  return response.data;
};

export const getMe = async (): Promise<UserOut> => {
  const response = await axiosClient.get(`/me`);

  return response.data;
};
