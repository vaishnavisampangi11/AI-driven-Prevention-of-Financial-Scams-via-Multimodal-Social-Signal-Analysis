import { Link, NavLink, useLocation, useNavigate } from 'react-router-dom'
import { Bell, FileText, History, LayoutDashboard, LogOut, ScanSearch, Search, ShieldCheck, UserRound } from 'lucide-react'
import { useState } from 'react'

const links = [
  { to: '/dashboard', label: 'Dashboard', Icon: LayoutDashboard },
  { to: '/analysis', label: 'Analysis', Icon: ScanSearch },
  { to: '/history', label: 'History', Icon: History },
  { to: '/alerts', label: 'Alerts', Icon: Bell },
  { to: '/reports', label: 'Reports', Icon: FileText },
  { to: '/profile', label: 'Profile', Icon: UserRound },
]

const pageTitles = {
  '/dashboard': 'Dashboard',
  '/analysis': 'Analysis workspace',
  '/history': 'Analysis history',
  '/alerts': 'Alerts & notifications',
  '/reports': 'Analysis report',
  '/profile': 'My profile',
}

export default function AppLayout({ children, title }) {
  const location = useLocation()
  const navigate = useNavigate()
  const displayName = localStorage.getItem('user_name') || 'SafeScan user'
  const [searchValue, setSearchValue] = useState('')

  const handleSearch = (event) => {
    event.preventDefault()
    const query = searchValue.trim()
    if (query) navigate(`/analysis?query=${encodeURIComponent(query)}`)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_name')
    navigate('/login')
  }

  return (
    <div className="app-shell app-layout">
      <aside className="app-sidebar">
        <Link className="sidebar-brand" to="/dashboard">
          <span className="shield-mark"><ShieldCheck size={20} strokeWidth={2.5} /></span>
          <span>SafeScan</span>
        </Link>
        <div className="sidebar-caption">WORKSPACE</div>
        <nav className="sidebar-nav" aria-label="Main navigation">
          {links.map((item) => (
            <NavLink key={item.to} to={item.to} className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}>
              <span className="sidebar-icon" aria-hidden="true"><item.Icon size={16} strokeWidth={1.8} /></span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <button className="sidebar-logout" type="button" onClick={logout}>
          <span className="sidebar-icon" aria-hidden="true"><LogOut size={16} strokeWidth={1.8} /></span> Log out
        </button>
      </aside>

      <div className="app-content">
        <header className="workspace-header">
          <div className="workspace-heading">
            <span className="workspace-kicker">SAFESCAN SECURITY CENTER</span>
            <h1>{title || pageTitles[location.pathname] || 'SafeScan'}</h1>
          </div>
          <form className="header-search" role="search" onSubmit={handleSearch}>
            <Search size={17} aria-hidden="true" />
            <input type="search" value={searchValue} onChange={(event) => setSearchValue(event.target.value)} placeholder="Search analysis, URL, or QR code..." aria-label="Search SafeScan" />
          </form>
          <div className="header-actions">
            <Link className="header-alert" to="/alerts" aria-label="View alerts" title="View alerts"><Bell size={17} strokeWidth={1.8} /></Link>
            <Link className="user-chip" to="/profile">
              <span className="user-avatar">{displayName.slice(0, 1).toUpperCase()}</span>
              <span className="user-chip-name">{displayName}</span>
            </Link>
          </div>
        </header>
        <main className="workspace-main">{children}</main>
        <footer className="workspace-footer"><span>SafeScan</span><span>Smarter Detection&nbsp; · &nbsp;Safer Transactions&nbsp; · &nbsp;A Secure Digital Future</span></footer>
      </div>
    </div>
  )
}