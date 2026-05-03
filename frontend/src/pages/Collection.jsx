import { useState, useEffect } from 'react'
import PageHero from '../components/PageHero'
import useFadeIn from '../components/useFadeIn'
import { vehiclesApi } from '../services/api'

const FILTERS = ['all', 'luxury', 'vintage', 'suv', 'convertible']

function CarCard({ car }) {
  return (
    <div className="car-card" data-tag={car.tag}>
      <div className="car-img">
        <span className="car-tag">{car.tag}</span>
        <img src={car.image_url} alt={car.name} loading="lazy" />
      </div>
      <div className="car-info">
        <div className="car-name">{car.name}</div>
        <div className="car-sub">{car.sub}</div>
        <div className="car-foot">
          <div className="car-price">
            Rs. {car.price.toLocaleString()}
            <small>/ 4hr</small>
          </div>
          <div className="car-arrow">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M1 7H13M13 7L7 1M13 7L7 13" stroke="currentColor" strokeWidth="1.4" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function Collection() {
  useFadeIn()

  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeFilter, setActiveFilter] = useState('all')
  const [maxPrice, setMaxPrice] = useState(200000)

  useEffect(() => {
    setLoading(true)
    vehiclesApi
      .list({ tag: activeFilter, max_price: maxPrice })
      .then(setVehicles)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [activeFilter, maxPrice])

  return (
    <>
      <PageHero
        eyebrow="The Full Collection"
        title="Browse the<br/><em>complete fleet</em>"
        lead="Filter by character. Every vehicle includes a chauffeur, fuel, and complimentary white floral dressing."
        bgImage="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=2000&q=80"
      />

      <section id="fleet">
        <div className="container">
          <div className="filters fade">
            {FILTERS.map(f => (
              <button
                key={f}
                className={`chip${activeFilter === f ? ' active' : ''}`}
                onClick={() => setActiveFilter(f)}
              >
                {f === 'all' ? 'All' : f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}

            <div className="filter-sep" />

            <div className="price-range">
              <span>Up to</span>
              <input
                type="range"
                min={30000}
                max={200000}
                step={5000}
                value={maxPrice}
                onChange={e => setMaxPrice(+e.target.value)}
              />
              <span>Rs. {maxPrice.toLocaleString()}</span>
            </div>
          </div>

          <div className="collection-grid fade">
            {loading && (
              <div className="empty-state" style={{ opacity: 0.6 }}>
                Loading the fleet…
              </div>
            )}
            {error && (
              <div className="empty-state" style={{ color: '#e88' }}>
                {error}
              </div>
            )}
            {!loading && !error && vehicles.length === 0 && (
              <div className="empty-state">
                No motorcars match those filters — adjust to see more.
              </div>
            )}
            {!loading && !error && vehicles.map(car => (
              <CarCard key={car.id} car={car} />
            ))}
          </div>
        </div>
      </section>
    </>
  )
}
