<div align="center">
  <br />
  <h1 align="center">J A T R A &nbsp;&nbsp; I Q</h1>
  <p align="center">
    <i>An Enterprise-Grade Meteorological Intelligence & Travel Optimization Platform</i>
  </p>
  <br />
  
  [![Live App](https://img.shields.io/badge/Live-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://jatra-iq.lovable.app)
  [![Google Sheets](https://img.shields.io/badge/Google_Sheets-109D59?style=for-the-badge&logo=googlesheets&logoColor=white)](https://docs.google.com/spreadsheets/d/1hwFGmLEbdN9G18Bwxb68edBSzJVwc3HRmfOlug9bFLI/edit?usp=sharing)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech/)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
</div>

<br />

> **🚀 Live:** [jatra-iq.lovable.app](https://jatra-iq.lovable.app)  
> **📊 Google Sheet:** [View Real-Time Data](https://docs.google.com/spreadsheets/d/1hwFGmLEbdN9G18Bwxb68edBSzJVwc3HRmfOlug9bFLI/edit?usp=sharing)  
> **⚙️ API Docs:** [jatraiq-api.up.railway.app/docs](https://jatraiq-api.up.railway.app/docs)

---

## 📌 Executive Summary

**JatraIQ** is a full-stack, cloud-native data engineering platform built to solve the complexity of travel planning in highly volatile meteorological regions like the Bengal delta. By continuously ingesting, normalizing, and analyzing severe weather and PM2.5 air quality fluctuations, JatraIQ provides actionable intelligence to end-users through a seamless React-based interface and real-time spreadsheet syndication.

The system operates entirely autonomously using containerized background schedulers to perform Extract, Transform, Load (ETL) operations, and calculates a proprietary **Travel Readiness Score** to grade the safety and comfort of major cities.

---

## 🏗️ System Architecture & Data Flow

The repository is structured as a **Monorepo**, cleanly isolating the Python Backend (`/src`) from the Vite/React Frontend (`/frontend`). 

```mermaid
graph LR
    %% Data Sources
    API[OpenWeatherMap]

    %% Core Backend Pipeline
    subgraph Backend [FastAPI ETL Pipeline]
    Ingest[Async API Ingestion] --> Clean[Pandas Normalization]
    Clean --> Score[Feature Engineering & ML Readiness]
    Score --> DB[(NeonDB Serverless PostgreSQL)]
    Score --> GS[(Google Sheets Analytics)]
    DB --> REST[REST API Endpoints]
    end

    %% Frontend & External
    UI[React / Vite Interface]
    Stakeholders[Data Analysts / Stakeholders]

    %% Connections
    Cron((APScheduler)) -.->|Triggers Every 4 Hours| Ingest
    API -->|Raw JSON| Ingest
    REST -->|JSON Payload| UI
    GS -->|Live View| Stakeholders
```

---

## 💻 Core Technical Achievements

### 1. Robust Data Engineering & Google Sheets Sync
- **GCP Service Account Integration:** Engineered an automated syndication pipeline using `gspread` and `google-auth` to push clean Pandas DataFrames directly into a [Live Google Spreadsheet](https://docs.google.com/spreadsheets/d/1hwFGmLEbdN9G18Bwxb68edBSzJVwc3HRmfOlug9bFLI/edit?usp=sharing) every 4 hours. Includes dynamic header generation, frozen rows, and custom UI formatting via the API.
- **Asynchronous Ingestion Engine:** Designed a high-throughput fetcher using `httpx` and `asyncio` to concurrently ingest weather, 5-day forecasts, and exact Air Pollution metrics without blocking the primary thread.
- **Pandas-driven Processing Layer:** Flattens deeply nested API payloads, enforces boundary validation rules, and parses ISO timestamps into analytics-ready formats.

### 2. Custom Feature Engineering (Scoring Algorithm)
The platform evaluates raw data against optimal human-comfort baselines to generate a unified `overall_score` (0-100) and assigns a categorical risk level (`Excellent`, `Good`, `Moderate`, `Risky`). The algorithm weighs:
- **Temperature Deviation**: Absolute variance from an optimal 22°C baseline.
- **Humidity Penalty**: Weighted deduction for uncomfortable tropical humidity levels.
- **Precipitation Risk**: Inverted probability scale targeting 0% rain.
- **Air Quality Index (AQI)**: Heavy penalization for PM2.5 threshold breaches utilizing European standards.

### 3. Cloud-Native Infrastructure & CI/CD
- **Serverless Relational Data**: Engineered highly normalized relational schemas using **SQLAlchemy** connected to a serverless **NeonDB** instance via connection pooling.
- **Containerization**: Packaged the Python application using an optimized, multi-stage `python:3.11-slim` **Dockerfile**, minimizing the attack surface and deployment footprint.
- **Continuous Deployment**: Deployed natively to **Railway** via GitHub Actions, injecting runtime secrets (like the Google credentials JSON) dynamically to ensure zero sensitive data is committed to version control.

---

## 🚀 Developer Setup

### Prerequisites
- Python 3.11+
- Node.js & Bun
- PostgreSQL (or an active NeonDB connection string)

### Backend (FastAPI & Pipeline)
```bash
# 1. Initialize Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Configure Secrets (.env)
# OPENWEATHER_API_KEY=your_openweather_key
# DATABASE_URL=postgresql://user:password@ep-neondb-url...
# GOOGLE_CREDENTIALS_JSON='{...}'
# GOOGLE_SHEET_ID=your_sheet_id

# 4. Boot the Server (http://localhost:8000)
uvicorn main:app --reload
```

### Frontend (React / Vite)
```bash
# 1. Navigate to Frontend Workspace
cd frontend

# 2. Install Node Packages
bun install

# 3. Start Development Server (http://localhost:5173)
bun run dev
```



<br />
<div align="center">
  <i>Architected with precision. Open to Software Engineering and Data Engineering opportunities.</i>
</div>
