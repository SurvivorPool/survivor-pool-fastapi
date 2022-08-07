from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from enums import LeagueTypes
from db.base_class import Base


class League(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float)
    start_week = Column(Integer, nullable=False, default=1)
    completed = Column(Boolean, nullable=False, default=False)
    type_id = Column(UUID(as_uuid=True), ForeignKey("leaguetype.id"),
                     default=LeagueTypes.Standard.value, nullable=False)

    league_type = relationship("LeagueType")
    teams = relationship("PlayerTeam", order_by="desc(PlayerTeam.active), desc(PlayerTeam.streak)")