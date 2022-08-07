from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from enums import MessageTypes
from db.base_class import Base


class UserMessage(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=False)
    type_id = Column(UUID(as_uuid=True), ForeignKey("messagetype.id"), default=MessageTypes.Default)
    created_date = Column(DateTime(timezone=True), default=func.now())
    read = Column(Boolean, default=False, server_default="False", nullable=False)
    read_date = Column(DateTime(timezone=True))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), default=uuid.uuid4, nullable=False)

    message_type = relationship("MessageType")
    user = relationship("User")
