import { useState, useEffect } from 'react';
import { useAuth } from '../../../context/AuthContext';
import type { LoginUser } from '../../types/user';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const { login, getme } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState<LoginUser>({ email: '', password_hash: '' });
  const [error, setError] = useState('');
  const [token, setToken] = useState('');


  useEffect(() => {
    const accessToken = localStorage.getItem('token')
    if (!accessToken) return 
    setToken(accessToken);
  }, [])


  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(form);
      /// get access token

      const my_data = await getme(token);

      if(my_data.role='super_admin'){
        navigate('/superadmin/dashboard'); // Redirect to the super admin dashboard
      } else if(my_data.role='company_user') {
        navigate('/company/dashboard')
      } else {
        navigate('/user/dashboard')
      }

    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="w-full max-w-md p-8 bg-white shadow-lg rounded-lg border border-gray-200">
        <h2 className="text-2xl font-bold text-center text-blue-600 mb-6">Login</h2>
        {error && <p className="text-red-600 text-center mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
            className="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <input
            type="password"
            name="password_hash"
            placeholder="Password"
            value={form.password_hash}
            onChange={handleChange}
            required
            className="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            type="submit"
            className="py-2 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition-colors"
          >
            Login
          </button>
        </form>
        <p className="mt-4 text-center text-black text-sm">
          Don't have an account? <a href='/register' className="text-blue-600 cursor-pointer">Sign up</a>
        </p>
      </div>
    </div>
  );
};

export default Login;
