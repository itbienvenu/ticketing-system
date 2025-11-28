import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div
      style={{
        display: 'flex',
        height: '100vh',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
      }}
    >
      <h1 style={{ fontSize: '32px', fontWeight: 'bold' }}>404 - Page Not Found</h1>
      <p style={{ marginTop: '10px', fontSize: '18px', color: '#555' }}>
        The page you are looking for does not exist or has been moved.
      </p>

      <Link
        to="/login"
        style={{
          marginTop: '20px',
          padding: '10px 20px',
          backgroundColor: '#2d6cdf',
          color: '#fff',
          textDecoration: 'none',
          borderRadius: '6px',
        }}
      >
        Go Back to Login
      </Link>
    </div>
  );
};

export default NotFound;
