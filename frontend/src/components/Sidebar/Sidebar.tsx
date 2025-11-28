import { useAuth } from '../../../context/AuthContext';

interface SidebarProps {
  setActivePage: (page: string) => void;
}

const Sidebar = ({ setActivePage }: SidebarProps) => {
  const { user } = useAuth();

  let menuItems: { name: string; key: string }[] = [];

  if (user?.role === 'super_admin') {
    menuItems = [
      { name: 'Dashboard', key: 'home' },
      { name: 'Companies', key: 'companies' },
      { name: 'Staff', key: 'staff' },
    ];
  } else if (user?.role === 'company_admin') {
    menuItems = [
      { name: 'Dashboard', key: 'home' },
      { name: 'Tickets', key: 'tickets' },
    ];
  } else if (user?.role === 'user') {
    menuItems = [
      { name: 'Dashboard', key: 'home' },
      { name: 'Request Ticket', key: 'request-ticket' },
    ];
  }

  return (
    <aside
      style={{
        width: '200px',
        background: '#f0f0f0',
        padding: '1rem',
        height: '100vh',
      }}
    >
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {menuItems.map((item) => (
          <li
            key={item.name}
            style={{ marginBottom: '1rem', cursor: 'pointer' }}
            onClick={() => setActivePage(item.key)}
          >
            {item.name}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
