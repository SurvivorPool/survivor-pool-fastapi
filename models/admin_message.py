from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db.base_class import Base


class AdminMessage(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), default=uuid.uuid4, nullable=False)
    message = Column(String, nullable=False)
    show = Column(Boolean, default=True)
    type = Column(String)

    user = relationship("User")
