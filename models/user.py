from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db.base_class import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    email = Column(String)
    is_admin = Column(Boolean)
    picture_url = Column(String)
    receive_notifications = Column(Boolean)
    wins = Column(Integer)
    provider = Column(String, nullable=False, default="google")

    teams = relationship("PlayerTeam", back_populates="user")