import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer>
      <div className="footer-grid">
        <div className="footer-brand">
          <Link to="/" className="brand">
            Syelon <b>Wedding</b>
          </Link>
          <p>
            Sri Lanka's most quietly confident wedding car company. Eleven years of
            unblemished record, driven island-wide.
          </p>
        </div>

        <div className="footer-col">
          <h4>Explore</h4>
          <ul>
            <li><Link to="/collection">The Collection</Link></li>
            <li><Link to="/packages">Packages</Link></li>
            <li><Link to="/about">Our Story</Link></li>
            <li><Link to="/contact">Concierge</Link></li>
          </ul>
        </div>

        <div className="footer-col">
          <h4>Service</h4>
          <ul>
            <li><a href="#">Western Province</a></li>
            <li><a href="#">Hill Country</a></li>
            <li><a href="#">Southern Coast</a></li>
            <li><a href="#">Cultural Triangle</a></li>
          </ul>
        </div>

        <div className="footer-col">
          <h4>Legal</h4>
          <ul>
            <li><a href="#">Refund Policy</a></li>
            <li><a href="#">Terms of Hire</a></li>
            <li><a href="#">Privacy</a></li>
          </ul>
        </div>
      </div>

      <div className="copy">
        <div>© 2026 Syelon Wedding (Pvt) Ltd · Sri Lanka</div>
        <div>Designed in Colombo · Driven Island-wide</div>
      </div>
    </footer>
  )
}
