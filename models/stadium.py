from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db.base_class import Base


class Stadium(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(String, nullable=False)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    roof_type = Column(String, nullable=False)
