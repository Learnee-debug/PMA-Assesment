import { weatherInfo } from '../weatherCodes';

function dayLabel(dateStr, idx) {
  if (idx === 0) return 'Today';
  const d = new Date(dateStr);
  return d.toLocaleDateString(undefined, { weekday: 'short' });
}

export default function ForecastList({ forecast }) {
  if (!forecast || !forecast.time) return null;

  // First entry from Open-Meteo's 6-day pull is "today"; show the next 5.
  const days = forecast.time.slice(0, 5).map((date, i) => ({
    date,
    label: dayLabel(date, i),
    max: forecast.temperature_2m_max[i],
    min: forecast.temperature_2m_min[i],
    code: forecast.weather_code[i],
    pop: forecast.precipitation_probability_max?.[i],
  }));

  return (
    <div className="forecast-list">
      <h3>5-Day Forecast</h3>
      <div className="forecast-grid">
        {days.map((d) => {
          const info = weatherInfo(d.code);
          return (
            <div className="forecast-day" key={d.date}>
              <div className="forecast-day-label">{d.label}</div>
              <div className="forecast-icon" aria-hidden="true">{info.icon}</div>
              <div className="forecast-temps">
                <strong>{Math.round(d.max)}°</strong> / {Math.round(d.min)}°
              </div>
              {typeof d.pop === 'number' && <div className="forecast-pop">💧 {d.pop}%</div>}
            </div>
          );
        })}
      </div>
    </div>
  );
}
