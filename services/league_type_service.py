from sqlalchemy.orm import Session
import crud
from schemas.league_type import LeagueTypeCreate, LeagueTypeUpdate


class LeagueTypeService:
    def get_by_name(self, db: Session, name: str):
        return crud.league_type.get_by_name(db, name)

    def get_all(self, db: Session):
        return crud.league_type.get_multi(db)

    def create_league_type(self, db: Session, league_type_create: LeagueTypeCreate):
        return crud.league_type.create(db, obj_in=league_type_create)


league_type_service = LeagueTypeService()