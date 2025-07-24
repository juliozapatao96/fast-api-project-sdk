import sys
import os
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from app.core.database import engine
from app.models.models import Player, Performance, Team, League, TeamPlayer

# Crear sesión
SessionLocal = sessionmaker(bind=engine)

def load_csv_data():
    """Carga datos desde archivos CSV manteniendo el orden de dependencias"""

    session = SessionLocal()

    try:
        print("Iniciando carga de datos...")

        # Cargar Leagues
        print("Cargando leagues...")
        league_df = pd.read_csv('data/league_data.csv')

        for _, row in league_df.iterrows():
            league = League(
                league_id=row['league_id'],
                league_name=row['league_name'],
                scoring_type=row['scoring_type'],
                last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d').date()
            )
            session.add(league)

        session.commit()
        print(f"{len(league_df)} leagues cargadas")


    except Exception as e:
        print(f"Error durante la carga: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def verify_data_counts():
    """Verifica que los datos se cargaron correctamente"""

    session = SessionLocal()

    try:
        print("Verificación de los datos cargados...")
        print("="*40)

        league_count = session.query(League).count()

        print(f"Leagues: {league_count}")


    except Exception as e:
        print(f"Error en verificación: {e}")
    finally:
        session.close()

def clear_all_data():
    """Limpia las tablas (recarga de datos)"""

    session = SessionLocal()

    try:
        print("Limpiando todas las tablas")

        session.query(League).delete()

        session.commit()
        print("Tablas limpiadas")
    except Exception as e:
        print(f"Error limpiando datos: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == '__main__':
    clear_all_data()
    load_csv_data()
    verify_data_counts()
    

