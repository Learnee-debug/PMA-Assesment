import { useState } from 'react';

export default function LocationSearch({ onSearch, onUseMyLocation, loading }) {
  const [value, setValue] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    if (!value.trim()) return;
    onSearch(value.trim());
  }

  return (
    <form className="location-search" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="City, town, zip code, landmark, or 'lat,lon'..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        aria-label="Location"
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Searching...' : 'Get Weather'}
      </button>
      <button type="button" className="secondary" onClick={onUseMyLocation} disabled={loading}>
        📍 Use My Location
      </button>
    </form>
  );
}
