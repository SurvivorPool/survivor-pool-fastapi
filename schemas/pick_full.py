from schemas.pick import PickResponse
from schemas.player_team import PlayerTeamResponse
from schemas.nfl_team import NFLTeamResponse
from schemas.game import GameResponse


class PickResponseFull(PickResponse):
    player_team: PlayerTeamResponse
    nfl_team_info: NFLTeamResponse
    game: GameResponse
