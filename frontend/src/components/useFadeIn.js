import { useEffect } from 'react'

/**
 * Attaches an IntersectionObserver to every .fade element on the page.
 * Call once per page (or per layout mount).
 */
export default function useFadeIn() {
  useEffect(() => {
    const els = document.querySelectorAll('.fade')
    const io = new IntersectionObserver(
      entries => {
        entries.forEach(e => {
          if (e.isIntersecting) {
            e.target.classList.add('in')
            io.unobserve(e.target)
          }
        })
      },
      { threshold: 0.12 }
    )
    els.forEach(el => io.observe(el))
    return () => io.disconnect()
  }, [])
}
