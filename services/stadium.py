import httpx
from httpx import Response
from sqlalchemy.orm import Session

import crud
from schemas.stadium import StadiumCreate


class StadiumService:
    nfl_endpoint = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

    async def update_stadiums(self, db: Session, rss_feed: Response = None):
        if rss_feed is None:
            rss_feed = httpx.get(self.nfl_endpoint)

        json = rss_feed.json()

        events = json['events']

        for event in events:
            competitions = event['competitions']
            competition = competitions[0]

            stadium_info = competition['venue']
            stadium_model = crud.stadium.get(db, stadium_info['id'])

            if not stadium_model:
                stadium_create = StadiumCreate(
                    id=stadium_info['id'],
                    city=stadium_info['address']['city'],
                    name=stadium_info['fullName'],
                    state=stadium_info['address']['state'] if 'state' in stadium_info['address'] else ''
                )
                crud.stadium.create(db, obj_in=stadium_create)

    def get_stadiums(self, db: Session):
        return crud.stadium.get_multi(db=db)




stadium_service = StadiumService()