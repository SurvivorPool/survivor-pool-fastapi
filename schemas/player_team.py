from pydantic import BaseModel
from uuid import UUID
from schemas.user import UserResponse
from schemas.league import LeagueResponse


class PlayerTeamBase(BaseModel):
    league_id: UUID
    user_id: UUID
    name: str
    active: bool
    paid: bool
    streak: int


class PlayerTeamCreate(BaseModel):
    league_id: UUID
    user_id: UUID
    name: str


class AdminPlayerTeamUpdate(BaseModel):
    active: bool
    paid: bool


class PlayerTeamUpdate(BaseModel):
    name: str


class PlayerTeamInDBBase(PlayerTeamBase):
    id: UUID

    class Config:
        orm_mode = True


class PlayerTeamResponse(PlayerTeamInDBBase):
    ...


class PlayerTeamResponseFull(PlayerTeamResponse):
    user: UserResponse
    league: LeagueResponse


class PlayerTeamList(BaseModel):
    teams: list[PlayerTeamResponse]