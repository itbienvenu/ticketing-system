import  { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { UserOut, LoginUser, RegisterUser } from '../src/types/user';
import  { loginUser, registerUser, getMe } from '../src/api/auth';

interface AuthContextType {
  user: UserOut | null;
  token: string | null;
  login: (data: LoginUser) => Promise<void>;
  register: (data: RegisterUser) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserOut | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

  const login = async (data: LoginUser) => {
    const res = await loginUser(data);
    setUser(res.user);
    setToken(res.access_token);
    localStorage.setItem('token', res.access_token);
  };

  const register = async (data: RegisterUser) => {
    const res = await registerUser(data);
    // Optionally log in immediately after registration
    await login({ email: res.email, password_hash: data.password });
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
