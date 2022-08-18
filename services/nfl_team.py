import httpx
from httpx import Response
from sqlalchemy.orm import Session
import crud
from models.nfl_team import NFLTeam
from schemas.nfl_team import NFLTeamCreate


class NFLTeamService:
    nfl_endpoint = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

    async def update_nfl_teams(self, db: Session, rss_feed: Response = None) -> list[NFLTeam]:
        if rss_feed is None:
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
                self.add_team(db, home_team)

            if not away_team_model:
                self.add_team(db, away_team)

    def get_teams(self, db: Session):
        teams = crud.nfl_team.get_multi(db=db)
        return teams

    def add_team(self, db: Session, team: dict):
        team_info = team['team']
        nickname = ''
        if 'name' not in team_info:
            nickname = team_info['displayName']
        else:
            nickname = team_info['name']

        team_create = NFLTeamCreate(
            id=team['id'],
            abbreviation=team_info['abbreviation'],
            city_state=team_info['location'],
            full_name=team_info['displayName'],
            nickname=nickname
        )

        crud.nfl_team.create(db, obj_in=team_create)


nfl_team_service = NFLTeamService()


