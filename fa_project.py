from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.crud.crud import get_player, get_players, get_performances, get_league


SessionLocal = sessionmaker(bind=engine)

try:
    session = SessionLocal()
    player = get_player(session, 1002)
    print(player.first_name)
    # test get_players
    players = get_players(session, last_name="Crosby")
    print(f"player last name: {players[0].last_name}")

    performances = get_performances(session)
    print(f"performance fantasy points : {performances[0].fantasy_points}")

    league = get_league(session, 5001)
    print(f"league data: {league.league_name}")


except Exception as e:
    print(f"Error durante ejecución crud: {e}")
finally:
    session.close()