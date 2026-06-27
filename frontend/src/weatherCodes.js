// WMO weather codes -> emoji + label (https://open-meteo.com/en/docs)
const MAP = {
  0: { icon: '☀️', label: 'Clear sky' },
  1: { icon: '🌤️', label: 'Mainly clear' },
  2: { icon: '⛅', label: 'Partly cloudy' },
  3: { icon: '☁️', label: 'Overcast' },
  45: { icon: '🌫️', label: 'Fog' },
  48: { icon: '🌫️', label: 'Rime fog' },
  51: { icon: '🌦️', label: 'Light drizzle' },
  53: { icon: '🌦️', label: 'Drizzle' },
  55: { icon: '🌧️', label: 'Dense drizzle' },
  61: { icon: '🌧️', label: 'Light rain' },
  63: { icon: '🌧️', label: 'Rain' },
  65: { icon: '🌧️', label: 'Heavy rain' },
  71: { icon: '🌨️', label: 'Light snow' },
  73: { icon: '🌨️', label: 'Snow' },
  75: { icon: '❄️', label: 'Heavy snow' },
  80: { icon: '🌦️', label: 'Rain showers' },
  81: { icon: '🌧️', label: 'Rain showers' },
  82: { icon: '⛈️', label: 'Violent showers' },
  95: { icon: '⛈️', label: 'Thunderstorm' },
  96: { icon: '⛈️', label: 'Thunderstorm w/ hail' },
  99: { icon: '⛈️', label: 'Severe thunderstorm' },
};

export function weatherInfo(code) {
  return MAP[code] || { icon: '🌡️', label: 'Unknown' };
}
