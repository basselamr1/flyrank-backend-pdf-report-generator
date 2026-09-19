from datetime import datetime,timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException, status
import sqlite3
from generate_pdf import generate_pdf
from fastapi.responses import FileResponse

app = FastAPI()
DATABASE = "report.db"

def init_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_database()

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post('/reports', status_code = status.HTTP_201_CREATED)
def create_report():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    created_at = datetime.now(timezone.utc).isoformat()

    cursor.execute("""
        INSERT INTO reports (path, created_at)
        VALUES (?, ?)
    """, ("", created_at))

    report_id = cursor.lastrowid

    conn.commit()
    conn.close()

    pdf_path = generate_pdf(report_id)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reports
        SET path = ?
        WHERE id = ?
    """, (pdf_path, report_id))

    conn.commit()
    conn.close()

    return {
        "id": report_id,
        "file": f"/reports/{report_id}/file",
    }

@app.get("/reports/{report_id}")
async def get_report(report_id: int):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            path,
            created_at
        FROM reports
        WHERE id = ?
    """, (report_id,))

    report = cursor.fetchone()

    conn.close()

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    return {
        "id": report["id"],
        "path": report["path"],
        "created_at": report["created_at"],
        "file": f"/reports/{report['id']}/file",
    }

@app.get("/reports/{report_id}/file")
async def get_report_file(report_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT path
        FROM reports
        WHERE id = ?
    """, (report_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    pdf_path = Path(row[0])

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Report file not found",
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"report-{report_id}.pdf",
    )