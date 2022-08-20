from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.nfl_team import NFLTeam
from schemas.nfl_team import NFLTeamCreate, NFLTeamUpdate


class CRUDNFLTeam(CRUDBase[NFLTeam, NFLTeamCreate, NFLTeamUpdate]):
    def get_team_by_nickname(self, db: Session, nickname: str):
        return db.query(NFLTeam).filter_by(nickname=nickname).first()


nfl_team = CRUDNFLTeam(NFLTeam)
