from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db.base_class import Base


class Game(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    home_team_name = Column(String, ForeignKey("nflteam.nickname"), nullable=False)
    home_team_score = Column(Integer, default=0)
    away_team_name = Column(String, ForeignKey("nflteam.nickname"), nullable=False)
    away_team_score = Column(Integer, default=0)
    day_of_week = Column(String)
    game_date = Column(DateTime(timezone=True))
    quarter = Column(String)
    quarter_time = Column(String)
    week = Column(Integer)
    stadium_id = Column(UUID(as_uuid=True), ForeignKey("stadium.id"), nullable=False)

    home_team_info = relationship("NFLTeam", foreign_keys=[home_team_name])
    away_team_info = relationship("NFLTeam", foreign_keys=[away_team_name])
    stadium_info = relationship("Stadium")