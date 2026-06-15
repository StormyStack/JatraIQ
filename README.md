<div align="center">
  <br />
  <h1 align="center">J A T R A &nbsp;&nbsp; I Q</h1>
  <p align="center">
    <i>An Enterprise-Grade Meteorological Intelligence & Travel Optimization Platform</i>
  </p>
  <br />
  
  [![Live Deployment](https://img.shields.io/badge/Production-Live-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://jatra-iq.lovable.app)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech/)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
</div>

<br />

> **Production Frontend:** [jatra-iq.lovable.app](https://jatra-iq.lovable.app)  
> **API Documentation (Swagger UI):** [jatraiq-api.up.railway.app/docs](https://jatraiq-api.up.railway.app/docs) *(Note: Replace with your actual Railway domain)*

---

## 📌 Executive Summary

**JatraIQ** is a full-stack, cloud-native data engineering platform designed to solve the complexity of travel planning in the Bengal delta. By continuously ingesting, normalizing, and analyzing highly volatile meteorological data and severe PM2.5 air quality fluctuations, JatraIQ provides actionable intelligence to end-users through a seamless React-based interface. 

The system operates entirely autonomously, utilizing background schedulers to perform Extract, Transform, Load (ETL) operations, and calculates a proprietary **Travel Readiness Score** to grade the safety and comfort of major cities.

---

## 🏗️ System Architecture & Data Flow

The repository is structured as a **Monorepo**, cleanly isolating the Python Backend (`/src`) from the Vite/React Frontend (`/frontend`). 

```mermaid
graph LR
    %% Data Sources
    API[OpenWeatherMap]

    %% Core Backend Pipeline
    subgraph Backend [FastAPI Data Pipeline]
    Ingest[Async Ingestion] --> Clean[Pandas Processing]
    Clean --> Score[Feature Engineering]
    Score --> DB[(NeonDB PostgreSQL)]
    DB --> REST[REST API Endpoints]
    end

    %% Frontend
    UI[React / Vite Frontend]

    %% Connections
    Cron((APScheduler)) -.->|Triggers Hourly| Ingest
    API -->|Raw JSON| Ingest
    REST -->|JSON Payload| UI
```

---

## 💻 Core Technical Achievements

### 1. Automated ETL & Data Engineering
- Designed an **Asynchronous Ingestion Engine** using `httpx` and `asyncio` to concurrently fetch current weather, 5-day forecasts, and precise latitude/longitude-based Air Pollution metrics without blocking the primary thread.
- Implemented a **Pandas-driven Processing Layer** (`clean_data.py`) to flatten deeply nested JSON payloads, map features, apply boundary validation rules (e.g., dropping anomalous temperatures), and parse ISO timestamps into ML-ready formats.
- Integrated **APScheduler** directly into the FastAPI event loop, ensuring the database is populated with rich, historical time-series data every hour with zero manual intervention.

### 2. Custom Feature Engineering (Scoring Algorithm)
The platform evaluates raw data against optimal human-comfort baselines to generate a unified `overall_score` (0-100) and assigns a categorical risk level (`Excellent`, `Good`, `Moderate`, `Risky`). The algorithm calculates:
- **Temperature Deviation**: Absolute variance from an optimal 22°C baseline.
- **Humidity Penalty**: Weighted deduction for uncomfortable tropical humidity levels.
- **Precipitation Risk**: Inverted probability scale targeting 0% rain.
- **Air Quality Index (AQI)**: Heavy penalization for PM2.5 threshold breaches, utilizing European 1-5 indices.

### 3. Cloud-Native Infrastructure & Deployment
- **Database**: Engineered highly normalized relational schemas using **SQLAlchemy** connected to a serverless **NeonDB** instance via connection pooling.
- **Containerization**: Packaged the API using an optimized, multi-stage `python:3.11-slim` **Dockerfile**, minimizing the attack surface and image footprint.
- **CI/CD Configuration**: Deployed the Dockerized backend natively to **Railway**, utilizing `.dockerignore` and dynamic port binding (`$PORT`) for seamless continuous deployment.

---

## 🚀 Developer Setup

### Prerequisites
- Python 3.11+
- Node.js & Bun
- PostgreSQL (or an active NeonDB connection string)

### Backend (FastAPI)
```bash
# 1. Initialize Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Configure Secrets (.env)
# OPENWEATHER_API_KEY=your_openweather_key
# DATABASE_URL=postgresql://user:password@ep-neondb-url...

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

---

## 🔮 Machine Learning Readiness (Phase 8 Roadmap)
By maintaining a strict separation between raw `weather_readings` and derived `travel_readiness` tables, the NeonDB database is primed for predictive modeling. Future iterations will utilize this historical corpus to train time-series forecasting models (e.g., ARIMA, Prophet, or LSTMs) to predict travel readiness weeks in advance.

<br />
<div align="center">
  <i>Architected with precision. Open to Software Engineering and Data Engineering opportunities.</i>
</div>
