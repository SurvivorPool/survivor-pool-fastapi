import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import Base


class NFLTeam(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    abbreviation = Column(String, nullable=False)
    city_state = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    conference = Column(String, nullable=False)
    division = Column(String, nullable=False)

