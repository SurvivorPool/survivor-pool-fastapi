from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from schemas.league_type import LeagueTypeResponse
from models.league import League
from models.league_type import LeagueType


class LeagueBase(BaseModel):
    name: str
    description: str
    price: float
    start_week: int
    completed: bool
    type_id: UUID


class LeagueCreate(LeagueBase):
    ...


class LeagueUpdate(BaseModel):
    id: UUID
    name: str
    description: str
    price: float


class LeagueInDBBase(LeagueBase):
    id: UUID

    class Config:
        orm_mode = True


class LeagueResponse(LeagueInDBBase):
    ...


class LeagueList(BaseModel):
    leagues: List[LeagueResponse]






