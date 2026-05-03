import { useEffect, useState } from 'react'
import { NavLink, Link } from 'react-router-dom'

const LINKS = [
  { to: '/', label: 'Home' },
  { to: '/collection', label: 'Collection' },
  { to: '/packages', label: 'Packages' },
  { to: '/about', label: 'About' },
  { to: '/contact', label: 'Contact' },
]

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 60)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    document.body.classList.toggle('locked', menuOpen)
  }, [menuOpen])

  const closeMenu = () => setMenuOpen(false)

  return (
    <>
      <nav className={`nav${scrolled ? ' scrolled' : ''}`}>
        <Link to="/" className="brand">
          Syelon <b>Wedding</b>
        </Link>

        <ul className="nav-links">
          {LINKS.map(({ to, label }) => (
            <li key={to}>
              <NavLink
                to={to}
                end={to === '/'}
                className={({ isActive }) => (isActive ? 'active' : '')}
              >
                {label}
              </NavLink>
            </li>
          ))}
        </ul>

        <Link to="/contact" className="btn-gold">
          <span>Reserve</span>
        </Link>

        <button
          className="nav-toggle"
          onClick={() => setMenuOpen(o => !o)}
          aria-label="Menu"
        >
          <span />
          <span />
          <span />
        </button>
      </nav>

      <div className={`mobile-nav${menuOpen ? ' open' : ''}`}>
        {LINKS.map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) => (isActive ? 'active' : '')}
            onClick={closeMenu}
          >
            {label}
          </NavLink>
        ))}
        <Link to="/contact" className="btn-gold" style={{ marginTop: 20 }} onClick={closeMenu}>
          <span>Reserve</span>
        </Link>
      </div>
    </>
  )
}
