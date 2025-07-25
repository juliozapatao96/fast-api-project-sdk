from app.core.database import engine, Base
from app.models import models

def recreate_tables():
    """Recrea las tablas de la base de datos (desarrollo rápido)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tablas recreadas con nueva estructura")

if __name__ == '__main__':
    recreate_tables()