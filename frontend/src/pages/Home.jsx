import { Link } from 'react-router-dom'
import useFadeIn from '../components/useFadeIn'

export default function Home() {
  useFadeIn()

  return (
    <section className="hero" id="home">
      <div className="hero-bg" />
      <div className="hero-content reveal">
        <div className="eyebrow left">Sri Lanka's Premier Wedding Fleet</div>
        <h1>
          Arrive Like <em>Royalty</em>
          <br />
          on Your Wedding Day
        </h1>
        <p className="lead">
          A handpicked collection of luxury, vintage and modern motorcars —
          chauffeured to make your most important day a moving picture of grace.
        </p>
        <div className="hero-cta">
          <Link to="/collection" className="btn-gold">
            <span>Explore the Fleet</span>
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M1 7H13M13 7L7 1M13 7L7 13" stroke="currentColor" strokeWidth="1.4" />
            </svg>
          </Link>
          <Link to="/contact" className="btn-ghost">
            <span>Reserve Your Date</span>
          </Link>
        </div>
      </div>

      <div className="hero-meta">
        <div className="num">12+</div>
        <div className="lbl">
          Marquee Vehicles
          <br />
          Across the Island
        </div>
      </div>
    </section>
  )
}
