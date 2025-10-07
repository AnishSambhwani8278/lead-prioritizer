# Lead Prioritizer API & Frontend

## Description

The **Lead Prioritizer** is a full-stack tool that helps sales and marketing teams **score and prioritize leads** from a CSV file.

* Backend: Flask API that parses CSV, scores leads based on title, email validity, company size, and location.
* Frontend: HTML + JS interface that uploads CSV, displays results in a table, and allows CSV download.
* Purpose: Save time by identifying high-value leads first.

---

## Features

* Upload CSV of leads
* Deduplicate entries
* Score leads by business-relevant criteria
* Display results in a sortable table
* Download prioritized CSV
* Frontend communicates with backend via REST API

---

## Project Structure

```
lead-prioritizer-api/
├─ backend/
│  ├─ app.py
│  ├─ requirements.txt
│  └─ sample_leads.csv
├─ frontend/
│  ├─ index.html
│  └─ main.js
└─ README.md
```

---

## Setup Instructions

### 1. Backend

1. Create and activate a virtual environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Flask server:

```bash
python app.py
```

The API runs at `http://127.0.0.1:5000/`.

### 2. Frontend

1. Open `frontend/index.html` in a browser.
2. Upload a CSV file and click **Upload & Score**.
3. View scored leads in the table and optionally download the CSV.

---

## Sample CSV

Use `backend/sample_leads.csv` or `backend/sample_leads_big.csv` to test the application.

---

## Notes

* The frontend and backend are **decoupled**, communicating only via API calls.
* NaN values in CSV are automatically converted to `null` for JSON compatibility.
* Scoring is deterministic and explainable: title, email quality, company size, and location.

