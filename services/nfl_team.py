import httpx
from sqlalchemy.orm import Session
from typing import List
import crud
from models.nfl_team import NFLTeam
from schemas.nfl_team import NFLTeamCreate


class NFLTeamService:
    nfl_endpoint = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

    async def get_nfl_teams(self, db: Session) -> List[NFLTeam]:
        rss_feed = httpx.get(self.nfl_endpoint)
        json = rss_feed.json()

        events = json['events']

        for event in events:
            competitions = event['competitions']
            teams = competitions[0]['competitors']

            home_team = next(filter(lambda team: team['homeAway'] == 'home', teams))
            away_team = next(filter(lambda team: team['homeAway'] == 'away', teams))

            home_team_model = crud.nfl_team.get(db, home_team['id'])
            away_team_model = crud.nfl_team.get(db, away_team['id'])

            if not home_team_model:
                home_info = home_team['team']
                nickname = ''
                if 'name' not in home_info:
                    nickname = home_info['displayName']
                else:
                    nickname = home_info['name']

                home_create = NFLTeamCreate(
                    id=home_team['id'],
                    abbreviation=home_info['abbreviation'],
                    city_state=home_info['location'],
                    full_name=home_info['displayName'],
                    nickname=nickname
                )

                crud.nfl_team.create(db, obj_in=home_create)


            if not away_team_model:
                away_info = away_team['team']
                nickname = ''
                if 'name' not in away_info:
                    nickname = away_info['displayName']
                else:
                    nickname = away_info['name']

                home_create = NFLTeamCreate(
                    id=away_team['id'],
                    abbreviation=away_info['abbreviation'],
                    city_state=away_info['location'],
                    full_name=away_info['displayName'],
                    nickname=nickname
                )

                crud.nfl_team.create(db, obj_in=home_create)
        teams = crud.nfl_team.get_multi(db=db)
        return teams


nfl_team_service = NFLTeamService()


