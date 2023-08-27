from pydantic import BaseModel
from typing import List
from uuid import UUID


class LeagueTypeBase(BaseModel):
    name: str
    description: str


class LeagueTypeCreate(LeagueTypeBase):
    ...


class LeagueTypeUpdate(LeagueTypeBase):
    id: UUID


class LeagueTypeInDBBase(LeagueTypeBase):
    class Config:
        from_attributes = True


class LeagueTypeResponse(LeagueTypeBase):
    id: UUID


class LeagueTypeList(BaseModel):
    league_types: List[LeagueTypeResponse]
