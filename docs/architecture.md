# Architecture

This project is built around a user-facing dashboard and a FastAPI backend that orchestrates the analysis flow.

1. User authenticates with JWT.
2. Frontend sends text, URL, or QR analysis requests.
3. FastAPI validates input, loads model artifacts, and routes through detectors.
4. AI modules generate probability outputs.
5. Risk engine normalizes scores and assigns levels.
6. Explanation engine builds evidence.
7. Decision engine outputs an action recommendation.
8. Data and alerts are saved to the database.
