from pydantic import BaseModel
from schemas.league import LeagueResponse
from schemas.pick import PickResponse
from schemas.player_team import PlayerTeamResponse
from schemas.user import UserResponse


class PlayerTeamResponseFull(PlayerTeamResponse):
    user: UserResponse
    league: LeagueResponse
    pick_history: list[PickResponse]


class PlayerTeamList(BaseModel):
    teams: list[PlayerTeamResponseFull]