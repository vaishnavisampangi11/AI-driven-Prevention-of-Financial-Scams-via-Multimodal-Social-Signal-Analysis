# AI-Driven Financial Scam Prevention System

## Project overview
This project is a final-year AI and cybersecurity application for detecting scam text messages, phishing URLs, and risky QR code content. It follows a practical architecture with a React frontend, FastAPI backend, PostgreSQL-ready storage, and lightweight ML models trained on small demo datasets.

## Problem statement
Financial scams increasingly exploit urgency, impersonation, fake links, and malicious QR codes. The system helps users assess the risk of suspicious content before they disclose sensitive data.

## Objectives
- Detect scam messages with a trained TF-IDF + logistic model
- Detect phishing URLs with URL feature extraction and a Random Forest model
- Decode QR images and assess embedded URL/text risk
- Persist results and alerts in a database
- Provide an interactive dashboard and history view
- Demonstrate a complete project suitable for final-year presentation

## Features
- JWT authentication for users
- Dashboard with real counts from the database
- Risk scoring and level classification
- Explanation generation based on actual risk signals
- Action and recommendation engine
- Alerts and report-style history
- Local file storage for uploads and reports
- Docker support for startup

## Architecture
The project implements the architecture described in the prompt: user -> auth -> React frontend -> FastAPI -> API gateway -> AI modules -> risk engine -> explanation engine -> decision engine -> database.

## Technology stack
- Frontend: React + Vite + JavaScript
- Backend: FastAPI + SQLAlchemy + JWT + Pydantic
- Database: PostgreSQL via SQLAlchemy and psycopg
- ML: scikit-learn, TF-IDF, Logistic Regression, Random Forest
- QR: pyzbar + Pillow
- Container: Docker Compose

## Project structure
- backend/
- frontend/
- data/
- scripts/
- docs/
- models/

## Installation
1. Create a virtual environment for the backend.
2. Install requirements:
   pip install -r backend/requirements.txt
3. Configure environment variables with backend/.env.example.
4. Start PostgreSQL with `docker compose up -d postgres`.
5. Migrate any existing SQLite data with `python scripts/migrate_sqlite_to_postgres.py`.
6. Start the backend with uvicorn and the frontend with `npm install` and `npm run dev`.

## PostgreSQL setup
PostgreSQL is the default database. Start it from the project root with `docker compose up -d postgres`, then install backend requirements and start the API. The local connection string is configured in `backend/.env`; Docker Compose supplies the database container hostname.

To preserve records from the previous SQLite database, install the updated requirements and run `python scripts/migrate_sqlite_to_postgres.py` once from the project root while PostgreSQL is running. The migration cancels if the PostgreSQL tables already contain rows. The original `backend/scam.db` is not modified or removed.

## Environment variables
See backend/.env.example.

## ML model training
Run the training scripts:
- python backend/ml/text_model/train.py
- python backend/ml/url_model/train.py

The dataset included is clearly labeled as demo/sample training data.

## Running backend
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
cd ..
python scripts/migrate_sqlite_to_postgres.py
cd backend
uvicorn app.main:app --reload --port 8000

## Running frontend
cd frontend
npm install
npm run dev

## Docker setup
From the project root:

docker compose up --build

## API documentation
FastAPI Swagger docs are available at http://localhost:8000/docs after starting the backend.

## Database structure
The main database tables include users, analyses, detection_results, alerts, and scam_cases.

## Testing
Run:

pytest

Note: the included tests are a baseline and should be expanded for production-grade validation.

## Troubleshooting
- Missing dependencies: reinstall requirements
- CORS errors: set CORS_ORIGINS correctly
- JWT issues: ensure the token is passed in the Authorization header
- QR decode problems: check that the uploaded image is valid and not corrupted

## Limitations
- Models use demo sample datasets for academic demonstration purposes
- This is not connected to real bank systems or live financial APIs
- The system performs application-level security analysis rather than real transaction interception

## Future enhancements
- Add stronger phishing features and larger training data
- Improve explainability with feature importance charts
- Add deep learning models for large-scale deployment
- Add PDF report generation
- Add email and WhatsApp integrations
