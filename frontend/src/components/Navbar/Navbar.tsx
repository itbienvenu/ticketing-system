import { useAuth } from '../../../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav style={{ padding: '1rem', background: '#333', color: '#fff', display: 'flex', justifyContent: 'space-between' }}>
      <span>Ticket Management System</span>
      <div>
        {user && (
          <>
            <span style={{ marginRight: '1rem' }}>{user.full_name} ({user.role})</span>
            <button onClick={logout} style={{ padding: '0.3rem 0.6rem', cursor: 'pointer' }}>Logout</button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
