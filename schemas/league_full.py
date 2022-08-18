from schemas.player_team import PlayerTeamResponse
from schemas.league_type import LeagueTypeResponse
from schemas.league import LeagueInDBBase


class LeagueResponseFull(LeagueInDBBase):
    # TODO: ADD LEAGUE TYPE AND TEAMS RELATIONSHIPS
    league_type: LeagueTypeResponse
    teams: list[PlayerTeamResponse]