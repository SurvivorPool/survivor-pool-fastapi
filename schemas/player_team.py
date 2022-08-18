from pydantic import BaseModel
from typing import List, Optional
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


class PlayerTeamUpdate(BaseModel):
    name: str


class PlayerTeamInDBBase(PlayerTeamBase):
    id: UUID


class PlayerTeamResponse(PlayerTeamInDBBase):
    ...


class PlayerTeamResponseFull(PlayerTeamResponse):
    user: UserResponse
    league: LeagueResponse


class PlayerTeamList(BaseModel):
    player_teams: List[PlayerTeamResponse]