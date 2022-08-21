from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.game import Game
from schemas.game import GameCreate, GameUpdate


class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate]):
    def get_games_by_week(self, db: Session, week_num: int) -> list[Game]:
        return db.query(Game).filter_by(week=week_num).all()

    def get_losers_for_week(self, db: Session, week_num: int) -> list[str]:
        game_models = self.get_games_by_week(db, week_num)
        losers = []
        for game_model in game_models:
            if game_model.home_team_score == game_model.away_team_score:
                losers.append(game_model.home_team_name)
                losers.append(game_model.away_team_name)
            elif game_model.home_team_score < game_model.away_team_score:
                losers.append(game_model.home_team_name)
            else:
                losers.append(game_model.away_team_name)

        return losers


game = CRUDGame(Game)
