from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from schemas.nfl_team import NFLTeamResponse
from schemas.odds import OddsResponse


class GameBase(BaseModel):
    id: int
    home_team_name: str
    home_team_score: int
    away_team_name: str
    away_team_score: int
    day_of_week: str
    game_date: datetime
    quarter: str
    quarter_time: str
    week: int


class GameCreate(GameBase):
    ...


class GameUpdate(BaseModel):
    id: int
    home_team_score: int
    away_team_score: int
    quarter: str
    quarter_time: str
    game_date: datetime
    day_of_week: str


class GameInDBBase(GameBase):
    class Config:
        from_attributes = True


class GameResponse(GameInDBBase):
    ...


class GameResponseFull(GameInDBBase):
    odds: Optional[OddsResponse]
    home_team_info: NFLTeamResponse
    away_team_info: NFLTeamResponse
    has_started: bool



class GameList(BaseModel):
    games: list[GameResponseFull]
