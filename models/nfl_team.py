import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import Base


class NFLTeam(Base):
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    abbreviation = Column(String, nullable=False)
    city_state = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    conference = Column(String, nullable=False, server_default="", default="")
    division = Column(String, nullable=False, server_default="", default="")

