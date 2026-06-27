import json
from urllib.parse import quote

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import exporters
from .db import get_connection, init_db
from .schemas import RecordCreate, RecordUpdate
from .validators import validate_date_range, validate_location_query
from .weather_api import (
    WeatherApiError,
    get_current_weather,
    get_five_day_forecast,
    get_weather_for_range,
    resolve_location,
)

app = FastAPI(title="Weather App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


def errors(messages: list[str], status: int) -> JSONResponse:
    return JSONResponse(status_code=status, content={"errors": messages})


def row_to_dict(row) -> dict:
    d = dict(row)
    d["weather"] = json.loads(d["weather_json"])
    return d


@app.get("/api/health")
def health():
    return {"status": "ok"}


# ---------- Live weather ----------


@app.get("/api/weather/lookup")
async def weather_lookup(location: str = ""):
    errs = validate_location_query(location)
    if errs:
        return errors(errs, 400)
    try:
        place = await resolve_location(location)
        current = await get_current_weather(place["latitude"], place["longitude"])
        forecast = await get_five_day_forecast(place["latitude"], place["longitude"])
        return {"place": place, "current": current["current"], "forecast": forecast["daily"]}
    except WeatherApiError as err:
        return errors([str(err)], 404)


@app.get("/api/weather/by-coords")
async def weather_by_coords(lat: float | None = None, lon: float | None = None):
    if lat is None or lon is None:
        return errors(["lat and lon are required and must be numeric"], 400)
    try:
        current = await get_current_weather(lat, lon)
        forecast = await get_five_day_forecast(lat, lon)
        return {
            "place": {"name": f"{lat:.4f}, {lon:.4f}", "latitude": lat, "longitude": lon},
            "current": current["current"],
            "forecast": forecast["daily"],
        }
    except WeatherApiError as err:
        return errors([str(err)], 502)


# ---------- CRUD ----------


@app.post("/api/records")
async def create_record(payload: RecordCreate):
    errs = validate_location_query(payload.location) + validate_date_range(payload.startDate, payload.endDate)
    if errs:
        return errors(errs, 400)

    try:
        place = await resolve_location(payload.location)
        weather = await get_weather_for_range(place["latitude"], place["longitude"], payload.startDate, payload.endDate)
    except WeatherApiError as err:
        return errors([str(err)], 422)

    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO records (location_query, resolved_name, latitude, longitude, start_date, end_date, weather_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload.location.strip(),
            place["name"],
            place["latitude"],
            place["longitude"],
            payload.startDate,
            payload.endDate,
            json.dumps(weather.get("daily", {})),
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM records WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return {"record": row_to_dict(row)}


@app.get("/api/records")
def list_records():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM records ORDER BY created_at DESC").fetchall()
    conn.close()
    return {"records": [row_to_dict(r) for r in rows]}


@app.get("/api/records/{record_id}")
def get_record(record_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
    conn.close()
    if not row:
        return errors(["Record not found"], 404)
    return {"record": row_to_dict(row)}


@app.put("/api/records/{record_id}")
async def update_record(record_id: int, payload: RecordUpdate):
    conn = get_connection()
    existing = conn.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
    if not existing:
        conn.close()
        return errors(["Record not found"], 404)

    location = payload.location if payload.location is not None else existing["location_query"]
    start_date = payload.startDate if payload.startDate is not None else existing["start_date"]
    end_date = payload.endDate if payload.endDate is not None else existing["end_date"]

    errs = validate_location_query(location) + validate_date_range(start_date, end_date)
    if errs:
        conn.close()
        return errors(errs, 400)

    try:
        location_changed = location != existing["location_query"]
        if location_changed:
            place = await resolve_location(location)
        else:
            place = {
                "name": existing["resolved_name"],
                "latitude": existing["latitude"],
                "longitude": existing["longitude"],
            }
        weather = await get_weather_for_range(place["latitude"], place["longitude"], start_date, end_date)
    except WeatherApiError as err:
        conn.close()
        return errors([str(err)], 422)

    conn.execute(
        """
        UPDATE records
        SET location_query = ?, resolved_name = ?, latitude = ?, longitude = ?,
            start_date = ?, end_date = ?, weather_json = ?, updated_at = datetime('now')
        WHERE id = ?
        """,
        (
            location.strip(),
            place["name"],
            place["latitude"],
            place["longitude"],
            start_date,
            end_date,
            json.dumps(weather.get("daily", {})),
            record_id,
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
    conn.close()
    return {"record": row_to_dict(row)}


@app.delete("/api/records/{record_id}")
def delete_record(record_id: int):
    conn = get_connection()
    cur = conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return errors(["Record not found"], 404)
    return Response(status_code=204)


# ---------- Export ----------


@app.get("/api/records/export/{fmt}")
def export_records(fmt: str):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM records ORDER BY created_at DESC").fetchall()
    conn.close()
    records = [dict(r) for r in rows]
    fmt = fmt.lower()

    if fmt == "json":
        return JSONResponse(
            content=records,
            headers={"Content-Disposition": 'attachment; filename="records.json"'},
        )
    if fmt == "csv":
        return Response(
            content=exporters.to_csv(records),
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="records.csv"'},
        )
    if fmt == "xml":
        return Response(
            content=exporters.to_xml(records),
            media_type="application/xml",
            headers={"Content-Disposition": 'attachment; filename="records.xml"'},
        )
    if fmt in ("md", "markdown"):
        return Response(
            content=exporters.to_markdown(records),
            media_type="text/markdown",
            headers={"Content-Disposition": 'attachment; filename="records.md"'},
        )
    if fmt == "pdf":
        return Response(
            content=exporters.to_pdf(records),
            media_type="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="records.pdf"'},
        )
    return errors([f'Unsupported format "{fmt}". Use json, csv, xml, md, or pdf.'], 400)


# ---------- Integrations ----------


@app.get("/api/integrations/youtube")
def youtube_integration(location: str = ""):
    if not location:
        return errors(["location is required"], 400)
    query = quote(f"{location} travel guide")
    return {"searchUrl": f"https://www.youtube.com/results?search_query={query}", "embedSearchQuery": query}


@app.get("/api/integrations/map")
def map_integration(lat: float | None = None, lon: float | None = None):
    if lat is None or lon is None:
        return errors(["lat and lon are required"], 400)
    delta = 0.05
    bbox = f"{lon - delta}%2C{lat - delta}%2C{lon + delta}%2C{lat + delta}"
    embed_url = f"https://www.openstreetmap.org/export/embed.html?bbox={bbox}&layer=mapnik&marker={lat}%2C{lon}"
    view_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=12/{lat}/{lon}"
    return {"embedUrl": embed_url, "viewUrl": view_url}
