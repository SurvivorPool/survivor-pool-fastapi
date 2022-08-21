from uuid import UUID
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.pick import Pick
from schemas.pick import PickCreate, PickUpdate


class CRUDPick(CRUDBase[Pick, PickCreate, PickUpdate]):
    def get_weekly_pick(self, db: Session, player_team_id: UUID, week_num: int):
        pick_model = db.query(Pick).filter_by(player_team_id=player_team_id, week_num=week_num).first()
        return pick_model

    def get_team_picks(self, db: Session, player_team_id: UUID):
        pick_models = db.query(Pick).filter_by(player_team_id=player_team_id).all()
        return pick_models

    def get_player_team_pick_for_week(self, db: Session, player_team_id: UUID, week_num: int) -> Pick:
        return db.query(Pick).filter_by(player_team_id=player_team_id, week_num=week_num).first()


pick = CRUDPick(Pick)