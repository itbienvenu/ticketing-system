import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
  children: ReactNode;
  allowedRoles?: string[];
}

const ProtectedRoute = ({ children, allowedRoles }: ProtectedRouteProps) => {
  const { user, token, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  // If not logged in, redirect to login
  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  // If allowedRoles is defined and user role is not included, redirect to login or 403 page
  if (allowedRoles && !allowedRoles.includes(user.role || '')) {
    return <Navigate to="/login" replace />;
  }

  // If all checks pass, render children
  return <>{children}</>;
};

export default ProtectedRoute;
