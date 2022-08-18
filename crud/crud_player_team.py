from uuid import UUID
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.player_team import PlayerTeam
from schemas.player_team import PlayerTeamCreate, PlayerTeamUpdate


class CRUDPlayerTeam(CRUDBase[PlayerTeam, PlayerTeamCreate, PlayerTeamUpdate]):
    def get_by_league_id(self, db: Session, league_id: UUID):
        return db.query(PlayerTeam).filter_by(league_id=league_id)

    def get_by_user_id(self, db: Session, user_id: UUID):
        return db.query(PlayerTeam).filter_by(user_id=user_id)


player_team = CRUDPlayerTeam(PlayerTeam)
