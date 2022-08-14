from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from schemas.odds import OddsResponse
from schemas.stadium import StadiumResponse


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
    stadium_id: int


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
    stadium_id: int


class GameInDBBase(GameBase):
    class Config:
        orm_mode = True


class GameResponse(GameInDBBase):
    odds: Optional[OddsResponse]
    stadium: Optional[StadiumResponse]


class GameList(BaseModel):
    games: List[GameResponse]
