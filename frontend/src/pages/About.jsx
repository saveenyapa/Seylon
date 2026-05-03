import { Link } from 'react-router-dom'
import PageHero from '../components/PageHero'
import useFadeIn from '../components/useFadeIn'
import useStatCounter from '../components/useStatCounter'

const STATS = [
  { count: 12, label: 'Marquee Vehicles' },
  { count: 6200, label: 'Weddings Served' },
  { count: 11, label: 'Years on the Road' },
  { count: 100, label: 'On-Time Record', suffix: '%' },
]

export default function About() {
  useFadeIn()
  useStatCounter()

  return (
    <>
      <PageHero
        eyebrow="Our Story"
        title="Eleven years.<br/>Six thousand <em>I-do's.</em>"
        lead="From a single garage in Battaramulla to the most quietly confident wedding fleet on the island."
        bgImage="https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=2000&q=80"
      />

      <section className="about" id="about" style={{ borderTop: 'none' }}>
        <div className="container">
          <div className="about-grid fade">
            <div className="about-img">
              <img
                src="https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=1200&q=80"
                alt="Vintage car detail"
              />
              <div className="about-quote">
                A wedding car should never simply transport. It should announce.
              </div>
            </div>

            <div className="about-info">
              <div className="eyebrow left">How It Began</div>
              <h2>
                One Mercedes.
                <br />
                One <em>chauffeur.</em>
              </h2>
              <p>
                <strong>Syelon Wedding</strong> began in a single garage in Battaramulla in 2014 —
                one Mercedes, one chauffeur, and an obsession with detail. Today our fleet roams
                the island from Galle Fort to the tea-country churches, dressing each car by hand
                the night before.
              </p>
              <p>
                We don't take more bookings than we can perfect. Our calendar caps at three
                weddings a day. The rest is mathematics.
              </p>
              <Link to="/contact" className="btn-ghost" style={{ marginTop: 14 }}>
                <span>Meet the Team</span>
              </Link>
            </div>
          </div>

          <div className="stats fade">
            {STATS.map(s => (
              <div key={s.label} className="stat">
                <div className="num" data-count={s.count} data-suffix={s.suffix || ''}>
                  0
                </div>
                <div className="lbl">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  )
}
