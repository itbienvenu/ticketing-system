import { Link } from 'react-router-dom';
import { useAuth } from '../../../context/AuthContext';

const Sidebar = () => {
  const { user } = useAuth();

  let menuItems: { name: string; path: string }[] = [];

  if (user?.role === 'superadmin') {
    menuItems = [
      { name: 'Dashboard', path: '/superadmin/dashboard' },
      { name: 'Companies', path: '/superadmin/companies' },
      { name: 'Staff', path: '/superadmin/staff' },
    ];
  } else if (user?.role === 'companyadmin') {
    menuItems = [
      { name: 'Dashboard', path: '/company/dashboard' },
      { name: 'Tickets', path: '/company/tickets' },
    ];
  } else if (user?.role === 'user') {
    menuItems = [
      { name: 'Dashboard', path: '/user/dashboard' },
      { name: 'Request Ticket', path: '/user/request-ticket' },
    ];
  }

  return (
    <aside style={{ width: '200px', background: '#f0f0f0', padding: '1rem', height: '100vh' }}>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {menuItems.map((item) => (
          <li key={item.name} style={{ marginBottom: '1rem' }}>
            <Link to={item.path}>{item.name}</Link>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
