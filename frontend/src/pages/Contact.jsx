import { useState } from 'react'
import PageHero from '../components/PageHero'
import useFadeIn from '../components/useFadeIn'
import { enquiriesApi, vehiclesApi } from '../services/api'

function PhoneIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4">
      <path d="M3 4 C3 3, 4 2, 5 2 H7 L9 6 L7 7 C8 9, 10 11, 12 12 L13 10 L17 12 V14 C17 15, 16 16, 15 16 C9 16, 3 11, 3 4 Z" />
    </svg>
  )
}

function EmailIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4">
      <path d="M2 4 H16 V14 H2 Z" />
      <path d="M2 4 L9 10 L16 4" />
    </svg>
  )
}

function SocialLinks() {
  return (
    <div className="socials">
      {[
        { label: 'Instagram', icon: <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4"><rect x="2" y="2" width="14" height="14" rx="4"/><circle cx="9" cy="9" r="3"/><circle cx="13" cy="5" r=".8" fill="currentColor"/></svg> },
        { label: 'Facebook', icon: <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4"><path d="M11 16 V9 H13 L13.5 6 H11 V4.5 C11 3.7, 11.3 3, 12.5 3 H13.7 V0.5 C13.5 0.5, 12.5 0.4, 11.5 0.4 C9 0.4, 8 1.7, 8 4.2 V6 H6 V9 H8 V16"/></svg> },
        { label: 'TikTok', icon: <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4"><path d="M11 2 V12 C11 13.6, 9.6 15, 8 15 S5 13.6, 5 12 S6.4 9, 8 9"/><path d="M11 2 C11 4, 12.5 6, 15 6"/></svg> },
        { label: 'YouTube', icon: <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4"><rect x="1" y="4" width="16" height="10" rx="3"/><path d="M7.5 7 L11 9 L7.5 11 Z" fill="currentColor"/></svg> },
      ].map(s => (
        <a key={s.label} href="#" aria-label={s.label}>{s.icon}</a>
      ))}
    </div>
  )
}

const EMPTY = {
  full_name: '', phone: '', wedding_date: '', vehicle_id: '',
  pickup_time: '', return_time: '', notes: '',
}

export default function Contact() {
  useFadeIn()

  const [form, setForm] = useState(EMPTY)
  const [vehicles, setVehicles] = useState([])
  const [submitting, setSubmitting] = useState(false)
  const [toast, setToast] = useState(null)

  // Load vehicles for the select dropdown
  useState(() => {
    vehiclesApi.list().then(setVehicles).catch(() => {})
  })

  const handleChange = e =>
    setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const showToast = (msg, ok = true) => {
    setToast({ msg, ok })
    setTimeout(() => setToast(null), 3500)
  }

  const handleSubmit = async e => {
    e.preventDefault()
    setSubmitting(true)
    try {
      await enquiriesApi.create({
        ...form,
        vehicle_id: form.vehicle_id ? parseInt(form.vehicle_id) : null,
      })
      showToast('Enquiry sent · we\'ll be in touch within 2 hours')
      setForm(EMPTY)
    } catch (err) {
      showToast(err.message, false)
    } finally {
      setSubmitting(false)
    }
  }

  const today = new Date().toISOString().split('T')[0]

  return (
    <>
      <PageHero
        eyebrow="Speak to the Concierge"
        title="We answer<br/>within <em>two hours.</em>"
        lead="Call or message us directly — our concierge team is available 7 days a week, 8am to 9pm."
        bgImage="https://images.unsplash.com/photo-1519440317898-a4d3fb6e286f?auto=format&fit=crop&w=2000&q=80"
      />

      <section id="contact">
        <div className="container">
          <div className="contact-grid fade">

            {/* Info card */}
            <div className="contact-info-card">
              <h3>Get in Touch</h3>
              <p>Available 7 days a week, 8am to 9pm.</p>

              <ul className="contact-list">
                <li>
                  <div className="ic"><PhoneIcon /></div>
                  <div>
                    <div className="lbl">Telephone</div>
                    <div className="val">+94 11 234 5678</div>
                  </div>
                </li>
                <li>
                  <div className="ic"><EmailIcon /></div>
                  <div>
                    <div className="lbl">Email</div>
                    <div className="val">concierge@syelon.lk</div>
                  </div>
                </li>
              </ul>

              <SocialLinks />
            </div>

            {/* Enquiry form */}
            <div className="contact-form-wrap">
              <form onSubmit={handleSubmit}>
                <div className="form-grid">
                  <div className="field">
                    <label>Full Name</label>
                    <input type="text" name="full_name" value={form.full_name}
                      onChange={handleChange} placeholder="e.g. Ravindi & Asanka" required />
                  </div>
                  <div className="field">
                    <label>Phone / WhatsApp</label>
                    <input type="tel" name="phone" value={form.phone}
                      onChange={handleChange} placeholder="+94 7..." required />
                  </div>
                  <div className="field">
                    <label>Wedding Date</label>
                    <input type="date" name="wedding_date" value={form.wedding_date}
                      onChange={handleChange} min={today} required />
                  </div>
                  <div className="field">
                    <label>Vehicle</label>
                    <select name="vehicle_id" value={form.vehicle_id} onChange={handleChange}>
                      <option value="">Select a motorcar</option>
                      {vehicles.map(v => (
                        <option key={v.id} value={v.id}>{v.name}</option>
                      ))}
                    </select>
                  </div>
                  <div className="field">
                    <label>Pickup Time</label>
                    <input type="time" name="pickup_time" value={form.pickup_time}
                      onChange={handleChange} required />
                  </div>
                  <div className="field">
                    <label>Return Time</label>
                    <input type="time" name="return_time" value={form.return_time}
                      onChange={handleChange} required />
                  </div>
                  <div className="field full">
                    <label>Special Requests</label>
                    <textarea name="notes" value={form.notes} onChange={handleChange}
                      rows={3} placeholder="Ribbon colour, music in the cabin, additional stops…" />
                  </div>
                </div>

                <div className="form-foot">
                  <small>By reserving, you accept our refund &amp; cancellation policy.</small>
                  <button type="submit" className="btn-gold" disabled={submitting}>
                    <span>{submitting ? 'Sending…' : 'Send Enquiry'}</span>
                    {!submitting && (
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <path d="M1 7H13M13 7L7 1M13 7L7 13" stroke="currentColor" strokeWidth="1.4" />
                      </svg>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </section>

      {toast && (
        <div className={`toast show`} style={{ background: toast.ok ? undefined : 'linear-gradient(135deg,#c44,#922)' }}>
          {toast.msg}
        </div>
      )}
    </>
  )
}
