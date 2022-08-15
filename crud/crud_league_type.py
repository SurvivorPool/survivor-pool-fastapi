from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.league_type import LeagueType
from schemas.league_type import LeagueTypeCreate, LeagueTypeUpdate


class CRUDLeagueType(CRUDBase[LeagueType, LeagueTypeCreate, LeagueTypeUpdate]):
    def get_by_name(self, db: Session, name: str):
        return db.query(LeagueType).filter_by(name=name).first()


league_type = CRUDLeagueType(LeagueType)

