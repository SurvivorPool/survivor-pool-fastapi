from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db.base_class import Base


class Stadium(Base):
    id = Column(Integer, nullable=False, primary_key=True, unique=True)
    city = Column(String, nullable=False)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    roof_type = Column(String, nullable=False)
