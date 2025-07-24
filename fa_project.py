from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.crud.crud import get_player


SessionLocal = sessionmaker(bind=engine)

try:
    session = SessionLocal()
    player = get_player(session, 1002)
    print(player.first_name)
except Exception as e:
    print(f"Error durante ejecución crud: {e}")
finally:
    session.close()