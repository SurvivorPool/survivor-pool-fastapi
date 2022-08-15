from pydantic import BaseModel
from typing import List
from uuid import UUID


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


class LeagueResponseFull(LeagueInDBBase):
    # TODO: ADD LEAGUE TYPE AND TEAMS RELATIONSHIPS
    pass


class LeagueList(BaseModel):
    leagues: List[LeagueResponse]






