import csv
import io

from dicttoxml import dicttoxml
from fpdf import FPDF

EXPORT_FIELDS = [
    "id",
    "location_query",
    "resolved_name",
    "latitude",
    "longitude",
    "start_date",
    "end_date",
    "created_at",
    "updated_at",
]


def to_csv(records: list[dict]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=EXPORT_FIELDS)
    writer.writeheader()
    for r in records:
        writer.writerow({k: r.get(k) for k in EXPORT_FIELDS})
    return output.getvalue()


def to_xml(records: list[dict]) -> bytes:
    trimmed = [{k: r.get(k) for k in EXPORT_FIELDS} for r in records]
    return dicttoxml(trimmed, custom_root="records", attr_type=False, item_func=lambda x: "record")


def to_markdown(records: list[dict]) -> str:
    header = "| ID | Location | Start | End | Resolved Name | Lat | Lon |\n|---|---|---|---|---|---|---|"
    rows = [
        f"| {r['id']} | {r['location_query']} | {r['start_date']} | {r['end_date']} | "
        f"{r['resolved_name']} | {r['latitude']} | {r['longitude']} |"
        for r in records
    ]
    return "\n".join([header, *rows])


def to_pdf(records: list[dict]) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Weather App - Saved Records", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.ln(2)
    for r in records:
        line = (
            f"#{r['id']} | {r['resolved_name']} | {r['start_date']} to {r['end_date']} | "
            f"({r['latitude']}, {r['longitude']})"
        )
        pdf.multi_cell(0, 7, line)
    return bytes(pdf.output())
