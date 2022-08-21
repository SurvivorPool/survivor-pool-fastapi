from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label

from crud.base import CRUDBase
from models.pick import Pick
from schemas.pick import PickCreate, PickUpdate
from services.game import game_service


class CRUDPick(CRUDBase[Pick, PickCreate, PickUpdate]):
    def get_weekly_pick(self, db: Session, player_team_id: UUID, week_num: int):
        pick_model = db.query(Pick).filter_by(player_team_id=player_team_id, week_num=week_num).first()
        return pick_model

    def get_team_picks(self, db: Session, player_team_id: UUID):
        pick_models = db.query(Pick).filter_by(player_team_id=player_team_id).all()
        return pick_models

    def get_player_team_pick_for_week(self, db: Session, player_team_id: UUID, week_num: int) -> Pick:
        return db.query(Pick).filter_by(player_team_id=player_team_id, week_num=week_num).first()

    def get_previous_week_picks_for_league(self, db: Session, league_id: UUID):
        prev_week_num = game_service.get_max_week(db) - 1
        return db.query(Pick.nfl_team_name, label('count', func.count(Pick.nfl_team_name))).filter_by(
            week_num=prev_week_num) \
            .join(Pick.player_team).filter_by(league_id=league_id).group_by(Pick.nfl_team_name).all()

    def get_all_picks(self, db: Session):
        prev_week_num = game_service.get_max_week(db) - 1
        return db.query(Pick.nfl_team_name, label('count', func.count(Pick.nfl_team_name))).filter_by(
            week_num=prev_week_num).group_by(Pick.nfl_team_name).all()


pick = CRUDPick(Pick)