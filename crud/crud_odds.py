from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.odds import Odds
from schemas.odds import OddsCreate, OddsUpdate


class CRUDOdds(CRUDBase[Odds, OddsCreate, OddsUpdate]):
    def get_by_game_id(self, db: Session, *, game_id: int):
        return db.query(Odds).filter(Odds.game_id == game_id).first()



odds = CRUDOdds(Odds)
