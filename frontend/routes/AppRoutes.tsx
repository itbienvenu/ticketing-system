import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from '../src/pages/auth/Login';
import Register from '../src/pages/auth/Register';
import NotFound from '../src/pages/NotFound'
import SuperAdminDashboard from '../src/pages/superAdmin/Dashboard';
import CompanyAdminDashboard from '../src/pages/companyAdmin/Dashboard';
import UserDashboard from '../src/pages/user/Dashboard';
import ProtectedRoute from './ProtectedRoute';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Super Admin */}
        <Route
          path="/superadmin/dashboard"
          element={
            <ProtectedRoute allowedRoles={['superadmin']}>
              <SuperAdminDashboard />
            </ProtectedRoute>
          }
        />

        {/* Company Admin */}
        <Route
          path="/company/dashboard"
          element={
            <ProtectedRoute allowedRoles={['companyadmin']}>
              <CompanyAdminDashboard />
            </ProtectedRoute>
          }
        />

        {/* User */}
        <Route
          path="/user/dashboard"
          element={
            <ProtectedRoute allowedRoles={['user']}>
              <UserDashboard />
            </ProtectedRoute>
          }
        />

        {/* 404 */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
