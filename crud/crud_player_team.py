from uuid import UUID
from typing import Union
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.player_team import PlayerTeam
from schemas.player_team import PlayerTeamCreate, PlayerTeamUpdate, AdminPlayerTeamUpdate


class CRUDPlayerTeam(CRUDBase[PlayerTeam, PlayerTeamCreate, PlayerTeamUpdate]):
    def get_by_league_id(self, db: Session, league_id: UUID):
        return db.query(PlayerTeam).filter_by(league_id=league_id)

    def get_by_user_id(self, db: Session, user_id: UUID):
        return db.query(PlayerTeam).filter_by(user_id=user_id)

    def get_active_teams(self, db: Session):
        return db.query(PlayerTeam).filter_by(active=True)

    def update(
        self,
        db: Session,
        *,
        db_obj: PlayerTeam,
        obj_in: Union[PlayerTeamUpdate, AdminPlayerTeamUpdate]
    ) -> PlayerTeam:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


player_team = CRUDPlayerTeam(PlayerTeam)
