from uuid import UUID

from sqlalchemy.orm import Session
from models import Game, Pick
from models.player_team import PlayerTeam
from schemas.pick import PickCreate, PickUpdate
from services.game import game_service
import crud


class PickService:

    def make_pick(self, db: Session, player_team_id: UUID, game_id: UUID, nfl_team_name: str) -> Pick:
        week_num = game_service.get_max_week(db)
        print(week_num)
        pick_model = crud.pick.get_weekly_pick(db, player_team_id, week_num)

        if not pick_model:
            pick_create_model = PickCreate(
                player_team_id=player_team_id,
                game_id=game_id,
                nfl_team_name=nfl_team_name,
                week_num=week_num
            )
            crud.pick.create(db=db, obj_in=pick_create_model)
        else:
            pick_update_model = PickUpdate(
                player_team_id=player_team_id,
                game_id=game_id,
                nfl_team_name=nfl_team_name
            )
            crud.pick.update(db=db, db_obj=pick_model, obj_in=pick_update_model)

        pick_model = crud.pick.get_weekly_pick(db, player_team_id, week_num)
        return pick_model

    def get_player_team_pick_for_week(self, db: Session, player_team_id: UUID, week_num: int) -> Pick:
        return crud.pick.get_player_team_pick_for_week(db, player_team_id, week_num)


pick_service = PickService()
