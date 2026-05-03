const BASE = '/api/v1'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  if (res.status === 204) return null
  return res.json()
}

// ── Vehicles ────────────────────────────────────────────────────────────────
export const vehiclesApi = {
  list: (params = {}) => {
    const qs = new URLSearchParams()
    if (params.tag && params.tag !== 'all') qs.set('tag', params.tag)
    if (params.max_price) qs.set('max_price', params.max_price)
    const query = qs.toString() ? `?${qs}` : ''
    return request(`/vehicles/${query}`)
  },
  get: (id) => request(`/vehicles/${id}`),
}

// ── Packages ─────────────────────────────────────────────────────────────────
export const packagesApi = {
  list: () => request('/packages/'),
  get: (id) => request(`/packages/${id}`),
}

// ── Enquiries ─────────────────────────────────────────────────────────────────
export const enquiriesApi = {
  create: (payload) =>
    request('/enquiries/', { method: 'POST', body: JSON.stringify(payload) }),
}
