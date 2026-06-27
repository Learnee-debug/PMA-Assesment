const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:4000/api';

async function request(path, options) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  const isJson = res.headers.get('content-type')?.includes('application/json');
  const body = isJson ? await res.json() : await res.text();
  if (!res.ok) {
    const message = (isJson && body.errors) ? body.errors.join('; ') : `Request failed (${res.status})`;
    throw new Error(message);
  }
  return body;
}

export const api = {
  lookupWeather: (location) => request(`/weather/lookup?location=${encodeURIComponent(location)}`),
  weatherByCoords: (lat, lon) => request(`/weather/by-coords?lat=${lat}&lon=${lon}`),

  listRecords: () => request('/records'),
  getRecord: (id) => request(`/records/${id}`),
  createRecord: (payload) => request('/records', { method: 'POST', body: JSON.stringify(payload) }),
  updateRecord: (id, payload) => request(`/records/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  deleteRecord: (id) => request(`/records/${id}`, { method: 'DELETE' }),

  exportUrl: (format) => `${BASE_URL}/records/export/${format}`,

  youtube: (location) => request(`/integrations/youtube?location=${encodeURIComponent(location)}`),
  map: (lat, lon) => request(`/integrations/map?lat=${lat}&lon=${lon}`),
};
