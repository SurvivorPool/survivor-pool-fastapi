from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from db.base_class import Base


class Odds(Base):
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    details = Column(String)
    over_under = Column(DECIMAL)

    game = relationship("Game", back_populates="odds_info")
