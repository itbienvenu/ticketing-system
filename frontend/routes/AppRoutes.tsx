import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from '../src/pages/auth/Login';
import Register from '../src/pages/auth/Register';
import NotFound from '../src/pages/NotFound';
import SuperAdminDashboard from '../src/pages/superAdmin/Dashboard';
import CompanyAdminDashboard from '../src/pages/companyAdmin/Dashboard';
import UserDashboard from '../src/pages/user/Dashboard';
import ProtectedRoute from './ProtectedRoute';

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/superadmin/dashboard"
          element={
            <ProtectedRoute allowedRoles={['super_admin']}>
              <SuperAdminDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/company/dashboard"
          element={
            <ProtectedRoute allowedRoles={['company_admin', 'company_user']}>
              <CompanyAdminDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/user/dashboard"
          element={
            <ProtectedRoute allowedRoles={['user']}>
              <UserDashboard />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
