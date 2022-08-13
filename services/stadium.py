import httpx
from sqlalchemy.orm import Session

from crud.crud_stadium import stadium


class StadiumService:
    nfl_endpoint = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

    async def update_stadiums(self, db: Session):
        rss_feed = httpx.get(self.nfl_endpoint)
        json = rss_feed.json()

        events = json['events']

        for event in events:
            competitions = event['competitions']
            competition = competitions[0]

            stadium_info = competition['venue']
            stadium_model = stadium.get(db, stadium_info['id'])
            print(stadium_model)



stadium_service = StadiumService()