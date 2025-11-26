import Navbar from '../../components/Navbar/Navbar';
import Sidebar from '../../components/Sidebar/Sidebar';

const CompanyAdminDashboard = () => {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Navbar />
        <main style={{ padding: '1rem' }}>
          <h1>Company Admin Dashboard</h1>
          <p>Manage tickets and assign permissions to your staff.</p>
        </main>
      </div>
    </div>
  );
};

export default CompanyAdminDashboard;
