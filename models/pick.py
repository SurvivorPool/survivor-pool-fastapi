from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db.base_class import Base


class Pick(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_team_id = Column(UUID(as_uuid=True), ForeignKey("playerteam.id"), default=uuid.uuid4, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    week_num = Column(Integer, nullable=False)
    nfl_team_name = Column(String, ForeignKey("nflteam.nickname"), nullable=False)

    player_team = relationship("PlayerTeam", back_populates="picks")
    game = relationship("Game")
    nfl_team_info = relationship("NFLTeam")