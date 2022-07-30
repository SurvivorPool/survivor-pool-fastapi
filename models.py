from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from enums import LeagueTypes, MessageTypes

Base = declarative_base()


class AdminMessage(Base):
    __tablename__ = "admin_message"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), default=uuid.uuid4, nullable=False)
    message = Column(String, nullable=False)
    show = Column(Boolean, default=True)
    type = Column(String)

    user = relationship("user")


class Game(Base):
    __tablename__ = "game"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    home_team_name = Column(String, ForeignKey("nfl_team.nickname"), nullable=False)
    home_team_score = Column(Integer, default=0)
    away_team_name = Column(String, ForeignKey("nfl_team.nickname"), nullable=False)
    away_team_score = Column(Integer, default=0)
    day_of_week = Column(String)
    game_date = Column(DateTime(timezone=True))
    quarter = Column(String)
    quarter_time = Column(String)
    week = Column(Integer)
    stadium_id = Column(UUID(as_uuid=True), ForeignKey("stadium.id"), nullable=False)

    home_team_info = relationship("nfl_team", foreign_keys=[home_team_name])
    away_team_info = relationship("nfl_team", foreign_keys=[away_team_name])
    stadium_info = relationship("stadium")


class League(Base):
    __tablename__ = "league"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float)
    start_week = Column(Integer, nullable=False, default=1)
    completed = Column(Boolean, nullable=False, default=False)
    type_id = Column(UUID(as_uuid=True), ForeignKey("league_type.id"),
                     default=LeagueTypes.Standard.value, nullable=False)

    league_type = relationship("league_type")
    teams = relationship("player_team", order_by="desc(player_team.is_active), desc(player_team.streak)")


class LeagueType(Base):
    __tablename__ = "league_type"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    description = Column(String)


class MessageType(Base):
    __tablename__ = "message_type"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)


class NFLTeam(Base):
    __tablename__ = "nfl_team"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    abbreviation = Column(String, nullable=False)
    city_state = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    conference = Column(String, nullable=False)
    division = Column(String, nullable=False)


class Pick(Base):
    __tablename__ = "pick"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_team_id = Column(UUID(as_uuid=True), ForeignKey("player_team.id"), default=uuid.uuid4, nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.id"), default=uuid.uuid4, nullable=False)
    week_num = Column(Integer, nullable=False)
    nfl_team_name = Column(String, ForeignKey("nfl_team.nickname"), nullable=False)

    player_team = relationship("player_team")
    game = relationship("game")
    nfl_team_info = relationship("nfl_team")


class PlayerTeam(Base):
    __tablename__ = "player_team"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    league_id = Column(UUID(as_uuid=True), ForeignKey("league.id"), default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    paid = Column(Boolean, default=False)
    streak = Column(Integer, default=0, server_default='0', nullable=False)

    user = relationship("user")
    league = relationship("league")


class Stadium(Base):
    __tablename__ = "stadium"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(String, nullable=False)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    roof_type = Column(String, nullable=False)


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    email = Column(String)
    is_admin = Column(Boolean)
    picture_url = Column(String)
    receive_notifications = Column(Boolean)
    wins = Column(Integer)

    teams = relationship("player_team")


class UserMessage(Base):
    __tablename__ = "user_message"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=False)
    type_id = Column(UUID(as_uuid=True), ForeignKey("message_type.id"), default=MessageTypes.Default)
    created_date = Column(DateTime(timezone=True), default=func.now())
    read = Column(Boolean, default=False, server_default="False", nullable=False)
    read_date = Column(DateTime(timezone=True))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), default=uuid.uuid4, nullable=False)

    message_type = relationship("message_type")
    user = relationship("user")
