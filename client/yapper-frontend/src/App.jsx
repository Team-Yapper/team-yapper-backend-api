import { Outlet, NavLink } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="nav-brand">
          <h1>Yapper</h1>
        </div>
        <ul className="nav-links">
          <li><NavLink to="/">Home</NavLink></li>
          <li><NavLink to="/create">Create Post</NavLink></li>
          <li><NavLink to="/profile">Profile</NavLink></li>
        </ul>
      </nav>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}

export default App
