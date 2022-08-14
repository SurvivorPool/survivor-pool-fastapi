from sqlalchemy.orm import Session
import crud


class OddsService:
    def get_by_id(self, db:Session, odds_id: int):
        return crud.odds.get(db, odds_id)


odds = OddsService()
