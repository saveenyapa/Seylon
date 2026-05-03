import { useEffect } from 'react'

function animateCount(el) {
  const target = +el.dataset.count
  const suffix = el.dataset.suffix || ''
  const dur = 1800
  const start = performance.now()
  const fmt = n => (n >= 1000 ? n.toLocaleString() : n)
  const tick = t => {
    const p = Math.min((t - start) / dur, 1)
    const eased = 1 - Math.pow(1 - p, 3)
    el.textContent = fmt(Math.round(target * eased)) + suffix
    if (p < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

export default function useStatCounter() {
  useEffect(() => {
    const els = document.querySelectorAll('.stat .num')
    const io = new IntersectionObserver(
      entries => {
        entries.forEach(e => {
          if (e.isIntersecting) {
            animateCount(e.target)
            io.unobserve(e.target)
          }
        })
      },
      { threshold: 0.4 }
    )
    els.forEach(el => io.observe(el))
    return () => io.disconnect()
  }, [])
}
