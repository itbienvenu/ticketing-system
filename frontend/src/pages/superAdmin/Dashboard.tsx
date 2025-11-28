import { useState } from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';

import DashboardHome from './views/DashboardHome';
import CompaniesList from './views/CompaniesList';
// import StaffList from './views/StaffList';

const SuperAdminDashboard = () => {
  const [activePage, setActivePage] = useState('home');

  const renderPage = () => {
    switch (activePage) {
      case 'companies':
        return <CompaniesList />;

      case 'staff':
        return <div>Staff List Page</div>;

      default:
        return <DashboardHome />;
    }
  };

  return (
    <div style={{ display: 'flex' }}>
      <Sidebar setActivePage={setActivePage} />

      <div style={{ flex: 1 }}>
        <Navbar />
        <main style={{ padding: '1rem' }}>{renderPage()}</main>
      </div>
    </div>
  );
};

export default SuperAdminDashboard;
