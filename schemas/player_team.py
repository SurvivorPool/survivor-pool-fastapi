from pydantic import BaseModel
from uuid import UUID

from schemas.pick import PickResponse
from schemas.user import UserResponse
from schemas.league import LeagueResponse


class PlayerTeamBase(BaseModel):
    league_id: UUID
    user_id: str
    name: str
    active: bool
    paid: bool
    streak: int


class PlayerTeamCreate(BaseModel):
    league_id: UUID
    user_id: str
    name: str


class AdminPlayerTeamUpdate(BaseModel):
    active: bool
    paid: bool


class AdminPlayerTeamAdvanceWeek(AdminPlayerTeamUpdate):
    streak: int


class PlayerTeamUpdate(BaseModel):
    name: str


class PlayerTeamInDBBase(PlayerTeamBase):
    id: UUID

    class Config:
        from_attributes = True


class PlayerTeamResponse(PlayerTeamInDBBase):
    current_pick: str


class AdvanceWeekResponse(BaseModel):
    deactivated_teams: list[PlayerTeamResponse]
    advancing_teams: list[PlayerTeamResponse]