from uuid import UUID
from sqlalchemy.orm import Session
import crud
from schemas.league import  LeagueCreate, LeagueUpdate


class LeagueService:
    def get_all(self, db: Session):
        return crud.league.get_multi(db)

    def get_by_id(self, db: Session, league_id: UUID):
        return crud.league.get(db, league_id)

    def create_league(self, db: Session, league_create_input: LeagueCreate):

        if league_create_input.type_id is None:
            standard_league_type = crud.league_type.get_by_name(db, "Standard")
            league_create_input.type_id = standard_league_type.id
        league_type_model = crud.league_type.get(db, league_create_input.type_id)
        if not league_type_model:
            raise Exception("League Type not found")
        if league_type_model.name == "Free":
            league_create_input.price = 0
        return crud.league.create(db, obj_in=league_create_input)

    def update_league(self, db: Session, league_update_input: LeagueUpdate):
        league_type_model = crud.league.get(db, league_update_input.id)
        if not league_type_model:
            raise Exception("League not found")
        if league_type_model.name == "Free":
            league_update_input.price = 0
        return crud.league.update(db, db_obj=league_type_model, obj_in=league_update_input)


league_service = LeagueService()
