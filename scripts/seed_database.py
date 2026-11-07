from app.database import SessionLocal
from app.models import User


def seed():
    db = SessionLocal()
    try:
        if not db.query(User).count():
            db.add(User(name='Demo User', email='demo@example.com', password_hash='demo'))
            db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    seed()
    print('Database seeded successfully.')
