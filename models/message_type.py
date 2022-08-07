from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db.base_class import Base


class MessageType(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
