import { Outlet, NavLink } from 'react-router-dom';
import '../styles/Layout.css';

const Layout = () => {
  return (
    <div className="layout">
      <header className="header">
        <div className="logo">Attendance<span>Report</span></div>
        <nav className="nav">
          <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>Home</NavLink>
          <NavLink to="/generate" className={({ isActive }) => isActive ? 'active' : ''}>Generate Report</NavLink>
          <NavLink to="/reference" className={({ isActive }) => isActive ? 'active' : ''}>Change Reference</NavLink>
          <NavLink to="/get" className={({ isActive }) => isActive ? 'active' : ''}>Get Report</NavLink>
        </nav>
      </header>
      <main className="main-content">
        <Outlet />
      </main>
      <footer className="footer">
        <p>© 2025 Attendance Report Generator. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;