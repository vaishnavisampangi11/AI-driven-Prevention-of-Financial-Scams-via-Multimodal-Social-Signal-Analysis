import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))
load_dotenv(BACKEND_ROOT / ".env")

from app.database import Base
from app import models


def main():
    source_path = BACKEND_ROOT / "scam.db"
    target_url = os.environ.get("DATABASE_URL")
    if not source_path.exists():
        raise SystemExit(f"SQLite database not found: {source_path}")
    if not target_url or not target_url.startswith("postgresql"):
        raise SystemExit("DATABASE_URL must point to PostgreSQL before migrating.")

    source_engine = create_engine(URL.create("sqlite", database=str(source_path)))
    target_engine = create_engine(target_url)
    Base.metadata.create_all(bind=target_engine)
    tables = Base.metadata.sorted_tables

    with source_engine.connect() as source, target_engine.begin() as target:
        existing_rows = {
            table.name: target.execute(select(func.count()).select_from(table)).scalar_one()
            for table in tables
        }
        if any(existing_rows.values()):
            raise SystemExit("PostgreSQL destination is not empty; migration cancelled.")

        migrated = {}
        for table in tables:
            records = source.execute(select(table)).mappings().all()
            if records:
                target.execute(table.insert(), [dict(record) for record in records])
            migrated[table.name] = len(records)

        for table in tables:
            if "id" in table.c and table.c.id.primary_key:
                target.execute(text(
                    f"SELECT setval(pg_get_serial_sequence('{table.name}', 'id'), "
                    f"COALESCE((SELECT MAX(id) FROM {table.name}), 1), "
                    f"EXISTS(SELECT 1 FROM {table.name}))"
                ))

    source_engine.dispose()
    target_engine.dispose()
    print("Migrated SQLite records to PostgreSQL:")
    for table_name, count in migrated.items():
        print(f"  {table_name}: {count}")


if __name__ == "__main__":
    main()