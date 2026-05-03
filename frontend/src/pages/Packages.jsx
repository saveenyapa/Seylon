import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import PageHero from '../components/PageHero'
import useFadeIn from '../components/useFadeIn'
import { packagesApi } from '../services/api'

const CheckIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4">
    <path d="M13 4 L6.5 11 L3 7.5" />
  </svg>
)

export default function Packages() {
  useFadeIn()

  const [packages, setPackages] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    packagesApi.list()
      .then(setPackages)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <>
      <PageHero
        eyebrow="Tailored Packages"
        title="Three ways to spend<br/>the <em>most important</em> day"
        lead="Each package includes chauffeur, fuel, dressing, white ribbons, and a chilled bottle of sparkling for the bridal party."
        bgImage="https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=2000&q=80"
      />

      <section id="packages">
        <div className="container">
          {loading && (
            <p style={{ color: 'var(--muted)', textAlign: 'center', padding: '60px 0' }}>
              Loading packages…
            </p>
          )}
          {error && (
            <p style={{ color: '#e88', textAlign: 'center', padding: '60px 0' }}>{error}</p>
          )}
          {!loading && !error && (
            <div className="packages-grid fade">
              {packages.map(pkg => (
                <div key={pkg.id} className={`pkg${pkg.is_featured ? ' featured' : ''}`}>
                  <div className="pkg-name">— {pkg.name}</div>
                  <div className="pkg-hours">
                    {pkg.hours}
                    <em>hrs</em>
                  </div>
                  <div className="pkg-desc">{pkg.description}</div>
                  <div className="pkg-price">
                    Rs. {pkg.price.toLocaleString()}
                    <small>&nbsp;from</small>
                  </div>
                  <ul className="pkg-list">
                    {pkg.features.map(f => (
                      <li key={f.id} className={f.included ? '' : 'dim'}>
                        <CheckIcon />
                        {f.text}
                      </li>
                    ))}
                  </ul>
                  <Link
                    to="/contact"
                    className={pkg.is_featured ? 'btn-gold' : 'btn-ghost'}
                    style={{ width: '100%', justifyContent: 'center' }}
                  >
                    <span>Reserve {pkg.name}</span>
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </>
  )
}
