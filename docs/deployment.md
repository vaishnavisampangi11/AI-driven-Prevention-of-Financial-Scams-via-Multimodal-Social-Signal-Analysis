# Deployment

## Local run
- Backend: uvicorn app.main:app --reload --port 8000
- Frontend: npm install && npm run dev

## Docker
- docker compose up --build

## Backup
- Use scripts/backup_db.sh or pg_dump in a configured PostgreSQL environment.
