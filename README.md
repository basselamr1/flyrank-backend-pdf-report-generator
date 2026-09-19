# PDF Report Generator

A FastAPI service that generates PDF reports from order data stored in SQLite. The API aggregates order information, renders the results as an HTML report, converts the HTML to a PDF using Playwright, and provides endpoints to retrieve generated reports.
## Dataset

The project uses a **synthetic orders dataset** stored in SQLite.

The `orders` table contains approximately 200 seeded orders with:

* `id`
* `customer`
* `product`
* `amount`
* `created_at`

The dataset is intentionally generated locally so the application can be run without downloading an external dataset.

## How to Run

### 1. Seed the database

From the project directory:

```powershell
uv run python seed.py
```

This creates/populates `report.db` with the synthetic order data.

### 2. Start the API

```powershell
uv run uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Report Aggregation SQL

The report uses SQLite aggregation queries to calculate the main report statistics.

Total orders:

```sql
SELECT COUNT(*) FROM orders;
```

Total revenue:

```sql
SELECT COALESCE(SUM(amount), 0) FROM orders;
```

Top products:

```sql
SELECT product, COUNT(*) AS order_count, SUM(amount) AS revenue
FROM orders
GROUP BY product
ORDER BY order_count DESC
LIMIT 5;
```

Orders per day:

```sql
SELECT DATE(created_at) AS day, COUNT(*) AS order_count
FROM orders
GROUP BY DATE(created_at)
ORDER BY day;
```

## Generate and Download a Report

Create a report:

```powershell
curl.exe -X POST http://127.0.0.1:8000/reports
```

The API returns the generated report ID and download link:

```json
{
  "id": 1,
  "file": "/reports/1/file"
}
```

Download the generated PDF:

```powershell
curl.exe -o report.pdf http://127.0.0.1:8000/reports/1/file
```

The generated PDF contains the report summary, top products, and order data.

### POST → Download Proof

Example successful flow:

```text
POST /reports
    ↓
201 Created
    ↓
{"id": 1, "file": "/reports/1/file"}
    ↓
GET /reports/1/file
    ↓
PDF file downloaded successfully
```

## Stage 4

The report endpoint generates a PDF from the aggregated order data and stores the generated file so it can be retrieved later using its report ID.

## Stage 5 — Idempotency

The duplicate-report check protects against repeated requests, such as double-clicks or accidental retries, generating multiple identical reports and files on the same day. In a real-world system, a missing idempotency check could cause a customer to receive the same email twice, resulting in duplicate processing and unnecessary costs.

When a report has already been generated today, another normal `POST /reports` returns the existing report with `200 OK` instead of generating another file.

A new report can still be explicitly requested with:

```powershell
curl.exe -X POST http://127.0.0.1:8000/reports `
  -H "Content-Type: application/json" `
  -d "{\"force\":true}"
```

## Generated PDF — Page 1

![Page 1 of generated PDF](reports/9.pdf)
