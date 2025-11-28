import  { createContext, use, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { UserOut, LoginUser, RegisterUser } from '../src/types/user';
import  { loginUser, registerUser, getMe } from '../src/api/auth';

interface AuthContextType {
  user: UserOut | null;
  token: string | null;
  loading: boolean;
  login: (data: LoginUser) => Promise<void>;
  register: (data: RegisterUser) => Promise<void>;
  getme: (token: string) => Promise<UserOut>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserOut | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [loading, setLoading] = useState<boolean>(true);
  
useEffect(() => {
  const checkAuth = async () => {
    try {
      setLoading(true);
      if (token) {
        const userData = await getMe();
        setUser(userData);
      }
    } catch (error) {
      setUser(null);
      setToken(null);
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  checkAuth();
}, []);

  const login = async (data: LoginUser) => {
    setLoading(true);
    const res = await loginUser(data);
    setToken(res.access_token);
    localStorage.setItem('token', res.access_token);

    await getme(); 
    setLoading(false);
  };

  const getme = async () => {
    const res = await getMe(); 
    setUser(res);
    return res;
  }


  const register = async (data: RegisterUser) => {
    await registerUser(data);
  };


  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, getme, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
