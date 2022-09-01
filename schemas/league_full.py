from pydantic import BaseModel

from schemas.player_team import PlayerTeamResponseFull
from schemas.league_type import LeagueTypeResponse
from schemas.league import LeagueResponse


class LeagueResponseFull(LeagueResponse):
    # TODO: ADD LEAGUE TYPE AND TEAMS RELATIONSHIPS
    league_type: LeagueTypeResponse
    teams: list[PlayerTeamResponseFull]


class LeagueListFull(BaseModel):
    leagues: list[LeagueResponseFull]