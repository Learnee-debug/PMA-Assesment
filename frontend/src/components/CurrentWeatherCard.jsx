import { weatherInfo } from '../weatherCodes';

export default function CurrentWeatherCard({ place, current }) {
  if (!current) return null;
  const info = weatherInfo(current.weather_code);

  return (
    <div className="current-card">
      <div className="current-card-main">
        <div className="current-icon" aria-hidden="true">{info.icon}</div>
        <div>
          <h2>{place.name}</h2>
          <p className="current-temp">{Math.round(current.temperature_2m)}°F</p>
          <p className="current-label">{info.label}</p>
        </div>
      </div>
      <div className="current-card-details">
        <div><span>Feels like</span><strong>{Math.round(current.apparent_temperature)}°F</strong></div>
        <div><span>Humidity</span><strong>{current.relative_humidity_2m}%</strong></div>
        <div><span>Wind</span><strong>{Math.round(current.wind_speed_10m)} mph</strong></div>
        <div><span>Precipitation</span><strong>{current.precipitation}"</strong></div>
      </div>
    </div>
  );
}
