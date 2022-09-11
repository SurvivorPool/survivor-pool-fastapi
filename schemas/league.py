from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class LeagueBase(BaseModel):
    name: str
    description: str
    price: float
    start_week: int
    completed: bool
    type_id: UUID


class LeagueCreate(BaseModel):
    name: str
    description: str
    price: float
    type_id: Optional[UUID] = None


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
    pot: float
    signup_active: bool


class LeagueList(BaseModel):
    leagues: list[LeagueResponse]






