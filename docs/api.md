# API Overview

## Authentication
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me

## Analysis
- POST /api/analyses/text
- POST /api/analyses/url
- POST /api/analyses/qr

## Dashboard
- GET /api/dashboard/summary

## History
- GET /api/analyses/history
- GET /api/analyses/{analysis_id}

## Alerts
- GET /api/alerts
- PATCH /api/alerts/{id}/read

## Profile
- GET /api/profile
- PUT /api/profile

## Health
- GET /health
- GET /health/db
