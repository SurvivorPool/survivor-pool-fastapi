from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db.base_class import Base


class User(Base):
    id = Column(String, primary_key=True)
    full_name = Column(String)
    email = Column(String)
    is_admin = Column(Boolean, server_default="False", default=False, nullable=False)
    picture_url = Column(String)
    receive_notifications = Column(Boolean, server_default="True", default=True, nullable=False)
    wins = Column(Integer, server_default="0", default=0, nullable=False)

    teams = relationship("PlayerTeam", back_populates="user")