import Navbar from '../../components/Navbar/Navbar';
import Sidebar from '../../components/Sidebar/Sidebar';

const UserDashboard = () => {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <div style={{ flex: 1 }}>
        <Navbar />
        <main style={{ padding: '1rem' }}>
          <h1>User Dashboard</h1>
          <p>Submit and track your tickets here.</p>
        </main>
      </div>
    </div>
  );
};

export default UserDashboard;
