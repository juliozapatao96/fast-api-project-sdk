from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.crud.crud import get_player, get_players


SessionLocal = sessionmaker(bind=engine)

try:
    session = SessionLocal()
    player = get_player(session, 1002)
    print(player.first_name)
    # test get_players
    players = get_players(session, last_name="Crosby")
    print(players[0].last_name)
except Exception as e:
    print(f"Error durante ejecución crud: {e}")
finally:
    session.close()