# 🌦️ Weather App — PM Accelerator Technical Assessment

**Author:** Shubham Padkonde
**Scope completed:** Tech Assessment #1 (Frontend) **and** Tech Assessment #2 (Backend) — submitted as a full-stack candidate.

A weather app that takes a location from the user, resolves it intelligently, and
surfaces real-time conditions, a 5-day forecast, contextual extras (map + travel
videos), and a database-backed history of saved lookups that can be exported in
five different formats.

---

## Table of Contents
- [Live features](#live-features)
- [Why these design choices](#why-these-design-choices)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [Environment variables](#environment-variables)
- [API reference](#api-reference)
- [Requirement → implementation map](#requirement--implementation-map)
- [Known limitations](#known-limitations)
- [About PM Accelerator](#about-pm-accelerator)

---

## Live features

**Frontend (Tech Assessment #1)**
- 🔎 Enter a location as a **city, town, zip/postal code, landmark, or raw GPS coordinates** (`lat,lon`) — one input field, no format you have to guess.
- 📍 **"Use My Location"** — one click, browser geolocation, current weather instantly.
- 🌡️ Current conditions: temperature, feels-like, humidity, wind, precipitation, and a weather icon.
- 📅 **5-day forecast** in a responsive card grid, with daily highs/lows, icons, and rain probability.
- 🗺️ Embedded map + ▶️ YouTube travel-video link for the resolved location.
- ⚠️ **Graceful error handling** — unrecognized location or a failed API call shows a dismissible banner instead of a blank screen or crash.
- 📱 **Fully responsive** — flexbox/grid layouts with breakpoints at 768px (tablet) and 480px (mobile); verified by hand at all three sizes.

**Backend (Tech Assessment #2)**
- 🗄️ **Full CRUD** on saved "location + date range" records, persisted in SQLite.
- ✅ **Validation** — date ranges must be well-formed, start ≤ end, span ≤ 1 year; locations are geocoded and rejected if they don't resolve (with fuzzy best-match for the rest).
- 🔌 **RESTful API** cleanly separating weather lookups (ephemeral) from saved records (persisted).
- 📤 **Export** all saved records to **JSON, CSV, XML, Markdown, or PDF** — pick any format from a single button bar.
- 🎥🗺️ **Third-party integrations** — YouTube search link and an OpenStreetMap embed for every resolved location.

## Why these design choices
A traveler checking the weather usually wants more than "is it sunny right now." They want
to know if it'll rain on the day they're actually traveling, what the next few days look
like, and they often don't know (or care about) the exact spelling/format of where they're
going — a city name, a zip code, or just "Eiffel Tower" should all work. That's why:

- **The location field is free text**, fuzzy-matched through a geocoder rather than a rigid dropdown.
- **"Use My Location"** covers the single most common real-world case — "what's it like right now, here" — without typing anything.
- **The save/CRUD flow is date-range based**, not single-day, because trip planning is about a window of time, not one moment.
- **Map + travel video links** answer the next question a traveler actually asks after the temperature: "what's this place even like?"

## Tech stack

| Layer | Choice | Notes |
|---|---|---|
| Frontend | **React 18 (Vite)**, plain CSS | No UI framework — flexbox/grid + media queries, per the assessment's JS-only frontend rule |
| Backend | **Python 3 + FastAPI** | Required language for the full-stack submission track |
| Database | **SQLite** (stdlib `sqlite3`) | Zero setup, file-based, ships with Python |
| Weather & geocoding | [Open-Meteo](https://open-meteo.com/) | Free, real-time, **no API key** |
| Map | OpenStreetMap embed | Free, **no API key** |
| Travel videos | YouTube search link | No API key/quota needed |

No API keys, secrets, or paid services are required to run this project end to end.

## Project structure
```
.
├── backend/                  # Tech Assessment #2 — Python / FastAPI
│   ├── app/
│   │   ├── main.py           # All REST routes (weather, CRUD, export, integrations)
│   │   ├── db.py             # SQLite connection + schema
│   │   ├── weather_api.py    # Open-Meteo geocoding / current / forecast / range calls
│   │   ├── validators.py     # Date-range & location validation
│   │   ├── exporters.py      # CSV / XML / Markdown / PDF builders
│   │   └── schemas.py        # Pydantic request models
│   ├── requirements.txt
│   ├── run.py                # Entry point (uvicorn)
│   └── README.md             # Backend-specific docs + full API reference
│
├── frontend/                  # Tech Assessment #1 — React (Vite)
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js                       # Fetch wrapper for every backend call
│   │   ├── weatherCodes.js              # WMO weather code → icon/label
│   │   ├── index.css                    # All styling, incl. responsive breakpoints
│   │   └── components/
│   │       ├── LocationSearch.jsx       # Input + "Use My Location"
│   │       ├── CurrentWeatherCard.jsx
│   │       ├── ForecastList.jsx         # 5-day grid
│   │       ├── ErrorBanner.jsx
│   │       ├── PlaceExtras.jsx          # Map + YouTube link
│   │       ├── RecordsManager.jsx       # CRUD UI + export buttons
│   │       └── PMAcceleratorInfo.jsx
│   ├── .env                  # VITE_API_BASE_URL
│   └── README.md             # Frontend-specific docs
│
└── README.md                  # ← you are here
```

## Getting started

**Requirements:** Python 3.10+ and Node.js 18+.

```bash
# Terminal 1 — backend (http://localhost:4000)
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
python run.py

# Terminal 2 — frontend (http://localhost:5173)
cd frontend
npm install
npm run dev
```

Then open **http://localhost:5173**. The SQLite file (`backend/weather.db`) is created
automatically on first run — no migration step needed. Interactive backend API docs are
available at **http://localhost:4000/docs** (FastAPI's built-in Swagger UI).

## Environment variables

| File | Variable | Default | Purpose |
|---|---|---|---|
| `frontend/.env` | `VITE_API_BASE_URL` | `http://localhost:4000/api` | Where the frontend sends API requests |

The backend needs no environment variables or API keys.

## API reference

Full reference with example payloads: [`backend/README.md`](backend/README.md).

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/weather/lookup?location=` | Current weather + 5-day forecast for a free-text location |
| GET | `/api/weather/by-coords?lat=&lon=` | Same, by raw coordinates (powers "Use My Location") |
| POST | `/api/records` | Create a saved record — `{ location, startDate, endDate }` |
| GET | `/api/records` | List all saved records |
| GET | `/api/records/{id}` | Get one record |
| PUT | `/api/records/{id}` | Update a record (partial body) |
| DELETE | `/api/records/{id}` | Delete a record |
| GET | `/api/records/export/{format}` | Export all records — `json`\|`csv`\|`xml`\|`md`\|`pdf` |
| GET | `/api/integrations/youtube?location=` | YouTube search URL for the location |
| GET | `/api/integrations/map?lat=&lon=` | OpenStreetMap embed/view URLs |

Every error response is shaped `{ "errors": ["..."] }` with an appropriate 4xx/5xx status,
so the frontend can render one consistent error banner regardless of which call failed.

## Requirement → implementation map

**Tech Assessment #1 — Frontend**
| Requirement | Where |
|---|---|
| Location input (city/zip/landmark/GPS) | [`LocationSearch.jsx`](frontend/src/components/LocationSearch.jsx) |
| Current-location weather | [`App.jsx`](frontend/src/App.jsx) `handleUseMyLocation` + `/api/weather/by-coords` |
| Weather shown clearly, with icons | [`CurrentWeatherCard.jsx`](frontend/src/components/CurrentWeatherCard.jsx), [`weatherCodes.js`](frontend/src/weatherCodes.js) |
| 5-day forecast (§1.1) | [`ForecastList.jsx`](frontend/src/components/ForecastList.jsx) |
| Error handling (§1.2) | [`ErrorBanner.jsx`](frontend/src/components/ErrorBanner.jsx) |
| Responsive across devices | [`index.css`](frontend/src/index.css) — flexbox/grid + breakpoints |
| Manages multiple backend APIs | [`api.js`](frontend/src/api.js) |

**Tech Assessment #2 — Backend (Python)**
| Requirement | Where |
|---|---|
| CREATE with date-range + location validation | [`main.py`](backend/app/main.py) `POST /api/records`, [`validators.py`](backend/app/validators.py) |
| READ (own + others' records) | `GET /api/records`, `/api/records/{id}` — no row-level security, as allowed |
| UPDATE with re-validation | `PUT /api/records/{id}` |
| DELETE | `DELETE /api/records/{id}` |
| RESTful API design | [`main.py`](backend/app/main.py) |
| Extra API integration (§2.2) | `/api/integrations/youtube`, `/api/integrations/map` |
| Data export (§2.3) | [`exporters.py`](backend/app/exporters.py) — JSON, CSV, XML, Markdown, PDF |

## Known limitations
- Open-Meteo's archive API has a short delay for the most recent ~5 days of historical data; very recent past dates in a saved record may occasionally return partial data.
- Geocoding takes the single top match for fuzzy queries — there's no disambiguation UI for genuinely ambiguous names (e.g., "Springfield").
- No authentication/row-level security, per the assessment's explicit instructions.

## About PM Accelerator
The Product Manager Accelerator Program is designed to support PM professionals through
every stage of their career. From students looking for entry-level jobs to Directors looking
to take on a leadership role, our program has helped over hundreds of students fulfill their
career aspirations. Our Product Manager Accelerator community includes Product Managers from
FAANG and Fortune 500 companies, sharing real-world insights and helping each other grow.

🔗 [PM Accelerator on LinkedIn](https://www.linkedin.com/school/pmaccelerator/)
