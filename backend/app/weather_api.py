import re
from datetime import date

import httpx

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

COORD_RE = re.compile(r"^(-?\d+(\.\d+)?)\s*,\s*(-?\d+(\.\d+)?)$")


class WeatherApiError(Exception):
    pass


async def resolve_location(query: str) -> dict:
    trimmed = query.strip()

    coord_match = COORD_RE.match(trimmed)
    if coord_match:
        lat = float(coord_match.group(1))
        lon = float(coord_match.group(3))
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            raise WeatherApiError("GPS coordinates out of range")
        return {"name": f"{lat:.4f}, {lon:.4f}", "latitude": lat, "longitude": lon}

    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(
            GEOCODE_URL,
            params={"name": trimmed, "count": 1, "language": "en", "format": "json"},
        )
        if res.status_code != 200:
            raise WeatherApiError("Geocoding service failed")
        data = res.json()

    results = data.get("results")
    if not results:
        raise WeatherApiError(f'Location "{query}" could not be found')

    top = results[0]
    parts = [top.get("name"), top.get("admin1"), top.get("country")]
    name = ", ".join(p for p in parts if p)
    return {"name": name, "latitude": top["latitude"], "longitude": top["longitude"]}


async def get_current_weather(lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "auto",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(FORECAST_URL, params=params)
        if res.status_code != 200:
            raise WeatherApiError("Weather service failed")
        return res.json()


async def get_five_day_forecast(lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code,wind_speed_10m_max",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "auto",
        "forecast_days": 6,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(FORECAST_URL, params=params)
        if res.status_code != 200:
            raise WeatherApiError("Forecast service failed")
        return res.json()


async def get_weather_for_range(lat: float, lon: float, start_date: str, end_date: str) -> dict:
    today = date.today().isoformat()
    is_past = end_date < today
    base_url = ARCHIVE_URL if is_past else FORECAST_URL
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "timezone": "auto",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(base_url, params=params)
        if res.status_code != 200:
            raise WeatherApiError("Weather range service failed")
        return res.json()
