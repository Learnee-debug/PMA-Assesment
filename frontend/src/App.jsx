import { useState } from 'react';
import { api } from './api';
import LocationSearch from './components/LocationSearch';
import CurrentWeatherCard from './components/CurrentWeatherCard';
import ForecastList from './components/ForecastList';
import ErrorBanner from './components/ErrorBanner';
import PlaceExtras from './components/PlaceExtras';
import RecordsManager from './components/RecordsManager';
import PMAcceleratorInfo from './components/PMAcceleratorInfo';

export default function App() {
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSearch(location) {
    setLoading(true);
    setError('');
    try {
      const data = await api.lookupWeather(location);
      setWeather(data);
    } catch (err) {
      setError(err.message);
      setWeather(null);
    } finally {
      setLoading(false);
    }
  }

  function handleUseMyLocation() {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by this browser.');
      return;
    }
    setLoading(true);
    setError('');
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          const data = await api.weatherByCoords(pos.coords.latitude, pos.coords.longitude);
          setWeather(data);
        } catch (err) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      },
      () => {
        setError('Unable to retrieve your location. Please check browser permissions.');
        setLoading(false);
      }
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌦️ Weather App</h1>
        <p className="muted">PM Accelerator Technical Assessment — by Shubham Padkonde</p>
      </header>

      <main>
        <LocationSearch onSearch={handleSearch} onUseMyLocation={handleUseMyLocation} loading={loading} />

        <ErrorBanner message={error} onDismiss={() => setError('')} />

        {weather && (
          <>
            <CurrentWeatherCard place={weather.place} current={weather.current} />
            <ForecastList forecast={weather.forecast} />
            <PlaceExtras place={weather.place} />
          </>
        )}

        <RecordsManager />
      </main>

      <PMAcceleratorInfo />
    </div>
  );
}
