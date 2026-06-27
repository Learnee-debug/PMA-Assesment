# Weather App — Frontend (Tech Assessment #1)

React (Vite) frontend. Plain CSS only — no UI framework, web-first/desktop-first
responsive layout with breakpoints for tablet (768px) and mobile (480px).

## Setup & Run
```bash
npm install
npm run dev      # http://localhost:5173
```
Requires the backend running at `http://localhost:4000` (see [../backend](../backend)),
or set `VITE_API_BASE_URL` in `.env` to point elsewhere.

## Structure
- `src/api.js` — thin fetch wrapper for all backend calls.
- `src/weatherCodes.js` — maps Open-Meteo's WMO weather codes to an emoji + label.
- `src/components/LocationSearch.jsx` — free-text location input + "Use My Location" (geolocation).
- `src/components/CurrentWeatherCard.jsx` — current conditions card.
- `src/components/ForecastList.jsx` — 5-day forecast grid.
- `src/components/ErrorBanner.jsx` — dismissible error banner (city not found / API failure).
- `src/components/PlaceExtras.jsx` — OpenStreetMap embed + YouTube travel-video search link for the resolved place.
- `src/components/RecordsManager.jsx` — CRUD UI against the backend's saved-records table, plus export links (JSON/CSV/XML/Markdown/PDF).
- `src/components/PMAcceleratorInfo.jsx` — author + PM Accelerator info footer.

## Responsive design
- Flexbox-based search bar and record form that wrap and stack to full-width columns under 480px.
- CSS grid forecast layout: 5 columns on desktop, 3 on tablet (≤768px), 2 on mobile (≤480px).
- `prefers-color-scheme` based light/dark theming via CSS variables.
