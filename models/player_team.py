from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db.base_class import Base


class PlayerTeam(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    league_id = Column(UUID(as_uuid=True), ForeignKey("league.id"), default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    paid = Column(Boolean, default=False)
    streak = Column(Integer, default=0, server_default='0', nullable=False)

    user = relationship("User", back_populates="teams")
    league = relationship("League", back_populates="teams")
