# PM Accelerator — Weather App (Full Stack Technical Assessment)

By **Shubham Padkonde**. Completes **both** Tech Assessment #1 (Frontend) and
Tech Assessment #2 (Backend).

A weather app where users can:
- Enter a location as city/town, zip/postal code, landmark, or raw GPS coordinates (`lat,lon`), and get current weather + a 5-day forecast.
- Use their browser's geolocation to get weather for "my current location."
- See a map of the resolved location and a YouTube search link for travel videos there.
- Save a location + date range to a database, then **read, update, and delete** those saved records (CRUD).
- **Export** all saved records as JSON, CSV, XML, Markdown, or PDF.

## Why this design
A traveler checking the weather for a trip usually cares about more than "is it sunny" —
they want to know if it'll rain on a specific travel day, what to expect a few days out,
and they may not know the exact spelling/format of where they're going (city name vs.
zip vs. "Eiffel Tower"). So the location field accepts free text and is fuzzy-matched via a
geocoder, "Use My Location" covers the common case of "what's it like right now, here,"
and the save/CRUD flow covers planning around a date range. Map + travel video links round
out trip planning beyond the raw temperature number.

## Stack
- **Frontend**: React (Vite), plain CSS (flexbox/grid + media queries, no framework) — JavaScript, not Python, per the frontend requirement.
- **Backend**: Python + FastAPI, SQLite (via the standard-library `sqlite3` module — no API keys to configure). Python was used here specifically to satisfy the full-stack-applicant requirement that Assessment #2 be done in Python.
- **Weather/Geocoding data**: [Open-Meteo](https://open-meteo.com/) — free, real-time, no API key.
- **Integrations**: OpenStreetMap embeds (no key) for maps; YouTube search links for travel videos.

## Running it
Requires **Node.js 18+** (frontend) and **Python 3.10+** (backend).

```bash
# Terminal 1 — backend
cd backend
python -m venv venv
venv\Scripts\activate        # Windows; use `source venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
python run.py                # http://localhost:4000

# Terminal 2 — frontend
cd frontend
npm install
npm run dev                  # http://localhost:5173
```

Open http://localhost:5173. The frontend talks to the backend via
`frontend/.env` (`VITE_API_BASE_URL`, defaults to `http://localhost:4000/api`).

See [backend/README.md](backend/README.md) for the full API reference and
[frontend](frontend/) for the component breakdown.

## Where each requirement is met

**Tech Assessment #1 (Frontend)**
- Location input (city/zip/landmark/GPS) + "Use My Location": [`frontend/src/components/LocationSearch.jsx`](frontend/src/components/LocationSearch.jsx), [`frontend/src/App.jsx`](frontend/src/App.jsx)
- Current weather with icons: [`frontend/src/components/CurrentWeatherCard.jsx`](frontend/src/components/CurrentWeatherCard.jsx), [`frontend/src/weatherCodes.js`](frontend/src/weatherCodes.js)
- 5-day forecast grid: [`frontend/src/components/ForecastList.jsx`](frontend/src/components/ForecastList.jsx)
- Error handling (city not found / API failure): [`frontend/src/components/ErrorBanner.jsx`](frontend/src/components/ErrorBanner.jsx)
- Responsive layout (flexbox/grid + breakpoints at 768px/480px): [`frontend/src/index.css`](frontend/src/index.css)
- Talks to multiple backend endpoints (weather, map, YouTube, records): [`frontend/src/api.js`](frontend/src/api.js)

**Tech Assessment #2 (Backend, Python/FastAPI)**
- CRUD with date-range + location validation: [`backend/app/main.py`](backend/app/main.py), [`backend/app/validators.py`](backend/app/validators.py)
- Persistence (SQLite via `sqlite3`): [`backend/app/db.py`](backend/app/db.py)
- RESTful API design: [`backend/app/main.py`](backend/app/main.py)
- Extra API integration (YouTube + Google-Maps-style embed via OSM): same file, `/api/integrations/*`
- Data export to JSON/CSV/XML/Markdown/PDF: [`backend/app/exporters.py`](backend/app/exporters.py)

## PM Accelerator
The Product Manager Accelerator Program is designed to support PM professionals through
every stage of their career. From students looking for entry-level jobs to Directors looking
to take on a leadership role, our program has helped over hundreds of students fulfill their
career aspirations. Our Product Manager Accelerator community includes Product Managers from
FAANG and Fortune 500 companies, sharing real-world insights and helping each other grow.
[LinkedIn](https://www.linkedin.com/school/pmaccelerator/)
