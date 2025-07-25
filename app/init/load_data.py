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
        print("\nCargando leagues...")
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

        # CARGAR TEAMS
        print("\nCargando teams...")
        team_df = pd.read_csv('data/team_data.csv')
        
        for _, row in team_df.iterrows():
            team = Team(
                team_id=row['team_id'],
                team_name=row['team_name'],
                league_id=row['league_id'],
                last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d').date()
            )
            session.add(team)
        
        session.commit()
        print(f"{len(team_df)} teams cargados")

        # CARGAR PLAYERS (sin dependencias directas)
        print("\nCargando players...")
        player_df = pd.read_csv('data/player_data.csv')
        
        for _, row in player_df.iterrows():
            player = Player(
                player_id=row['player_id'],
                gsis_id=row.get('gsis_id'),  # Puede ser nulo
                first_name=row['first_name'],
                last_name=row['last_name'],
                position=row['position'],
                last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d').date()
            )
            session.add(player)
        
        session.commit()
        print(f"{len(player_df)} players cargados")

        # CARGAR PERFORMANCES (depende de players)
        print("\nCargando performances...")
        performance_df = pd.read_csv('data/performance_data.csv')
        
        for _, row in performance_df.iterrows():
            performance = Performance(
                performance_id=row['performance_id'],
                week_number=str(row['week_number']),
                fantasy_points=float(row['fantasy_points']),
                player_id=row['player_id'],
                last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d').date()
            )
            session.add(performance)
        
        session.commit()
        print(f"{len(performance_df)} performances cargadas")
        
        # TEAM_PLAYER (depende de teams y players)
        print("\nCargando team_player relationships...")
        team_player_df = pd.read_csv('data/team_player_data.csv')
        
        for _, row in team_player_df.iterrows():
            team_player = TeamPlayer(
                team_id=row['team_id'],
                player_id=row['player_id'],
                last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d').date()
            )
            session.add(team_player)
        
        session.commit()
        print(f"{len(team_player_df)} team_player relationships cargadas")
        
        print("\n¡Todos los datos cargados exitosamente!")


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
        print("\nVerificación de los datos cargados...")
        print("="*40)

        league_count = session.query(League).count()
        team_count = session.query(Team).count()
        player_count = session.query(Player).count()
        performance_count = session.query(Performance).count()
        team_player_count = session.query(TeamPlayer).count()

        print(f"Leagues: {league_count}")
        print(f"Teams: {team_count}")
        print(f"Players: {player_count}")
        print(f"Performances: {performance_count}")
        print(f"Team-Player relationships: {team_player_count}")


    except Exception as e:
        print(f"Error en verificación: {e}")
    finally:
        session.close()

def clear_all_data():
    """Limpia las tablas (recarga de datos)"""

    session = SessionLocal()

    try:
        print("Limpiando todas las tablas")

        session.query(TeamPlayer).delete()
        session.query(Performance).delete()
        session.query(Player).delete()
        session.query(Team).delete()
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
    

