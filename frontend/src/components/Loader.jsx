import { useEffect, useState } from 'react'

export default function Loader() {
  const [hidden, setHidden] = useState(false)

  useEffect(() => {
    const t = setTimeout(() => setHidden(true), 1200)
    return () => clearTimeout(t)
  }, [])

  return (
    <div className={`loader${hidden ? ' hidden' : ''}`}>
      <div className="loader-mark">Syelon</div>
      <div className="loader-ring" />
      <div className="loader-tag">Wedding Cars</div>
    </div>
  )
}
