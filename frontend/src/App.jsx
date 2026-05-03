import { Routes, Route, useLocation } from 'react-router-dom'
import { useEffect } from 'react'

import Nav from './components/Nav'
import Footer from './components/Footer'
import WhatsAppFloat from './components/WhatsAppFloat'

import Home from './pages/Home'
import Collection from './pages/Collection'
import Packages from './pages/Packages'
import About from './pages/About'
import Contact from './pages/Contact'

function ScrollToTop() {
  const { pathname } = useLocation()
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])
  return null
}

export default function App() {
  return (
    <>
      <ScrollToTop />
      <Nav />
      <div className="grain" />

      <Routes>
        <Route path="/"           element={<Home />} />
        <Route path="/collection" element={<Collection />} />
        <Route path="/packages"   element={<Packages />} />
        <Route path="/about"      element={<About />} />
        <Route path="/contact"    element={<Contact />} />
      </Routes>

      <Footer />
      <WhatsAppFloat />
    </>
  )
}
