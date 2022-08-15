from crud.base import CRUDBase
from models.league import League
from schemas.league import LeagueCreate, LeagueUpdate


class CRUDLeague(CRUDBase[League, LeagueCreate, LeagueUpdate]):
    ...


league = CRUDLeague(League)