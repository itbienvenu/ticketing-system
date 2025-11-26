import Navbar from '../../components/Navbar/Navbar';
import Sidebar from '../../components/Sidebar/Sidebar';

const SuperAdminDashboard = () => {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Navbar />
        <main style={{ padding: '1rem' }}>
          <h1>Super Admin Dashboard</h1>
          <p>Welcome! Here you can manage companies and staff.</p>
        </main>
      </div>
    </div>
  );
};

export default SuperAdminDashboard;
