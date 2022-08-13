from crud.base import CRUDBase
from models.nfl_team import NFLTeam
from schemas.nfl_team import NFLTeamCreate, NFLTeamUpdate


class CRUDNFLTeam(CRUDBase[NFLTeam, NFLTeamCreate, NFLTeamUpdate]):
    ...


nfl_team = CRUDNFLTeam(NFLTeam)
