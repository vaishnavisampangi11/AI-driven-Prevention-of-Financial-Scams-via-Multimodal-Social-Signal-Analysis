# Database Documentation

The system stores users, analysis records, detection results, alerts, and scam case metadata.

## Main models
- User
- Analysis
- DetectionResult
- Alert
- ScamCase

## Notes
- SQLite is the default local database.
- PostgreSQL is supported via DATABASE_URL configuration.
- SQLAlchemy handles data creation and access.
