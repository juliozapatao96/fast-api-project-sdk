from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

class Player(Base):
    __tablename__ = "player"
    player_id = Column(Integer, primary_key=True, index=True)
    gsis_id = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)

class Performance(Base):
    __tablename__ = "performance"
    performance_id = Column(Integer, primary_key=True, index=True)
    week_number = Column(String, nullable=False)
    fantasy_points = Column(Float, nullable=False)
    player_id = Column(Integer, ForeignKey("player.player_id"), nullable=False)
    last_changed_date = Column(Date, nullable=False)


class TeamPlayer(Base):
    __tablename__="team_player"
    team_id = Column(Integer, ForeignKey("team.team_id"), primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.player_id"),primary_key=True, index=True)
    last_changed_date = Column(Date, nullable=False)

class Team(Base):
    __tablename__="team"
    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)
    league_id = Column(Integer, ForeignKey("league.league_id"))


class League(Base):
    __tablename__="league"
    league_id = Column(Integer, primary_key=True, index=True)
    league_name = Column(String, nullable=False)
    scoring_type = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)