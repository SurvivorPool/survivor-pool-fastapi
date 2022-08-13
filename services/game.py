import httpx
from sqlalchemy.orm import Session

from services.stadium import stadium_service


class GameService:
    nfl_endpoint = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

    async def update_games(self, db: Session):
        await stadium_service.update_stadiums(db)
        rss_feed = httpx.get(self.nfl_endpoint)


game_service = GameService()
