import httpx
from httpx import Response
from sqlalchemy.orm import Session
import crud
from models.nfl_team import NFLTeam
from schemas.nfl_team import NFLTeamCreate


class NFLTeamService:
    nfl_endpoint = 'https://site.api.espn.com/apis/v2/scoreboard/header?sport=football&league=nfl&lang=en&region=us&contentorigin=espn&tz=America%2FNew_York'

    async def update_nfl_teams(self, db: Session, rss_feed: Response = None) -> list[NFLTeam]:
        if rss_feed is None:
            rss_feed = httpx.get(self.nfl_endpoint)

        json = rss_feed.json()['sports'][0]['leagues'][0]

        events = json['events']

        for event in events:
            teams = event['competitors']

            home_team = next(filter(lambda team: team['homeAway'] == 'home', teams))
            away_team = next(filter(lambda team: team['homeAway'] == 'away', teams))

            home_team_model = crud.nfl_team.get(db, home_team['id'])
            away_team_model = crud.nfl_team.get(db, away_team['id'])

            if not home_team_model:
                self.add_team(db, home_team)

            if not away_team_model:
                self.add_team(db, away_team)

    def get_team_by_nickname(self, db: Session, nickname: str):
        return crud.nfl_team.get_team_by_nickname(db, nickname)

    def get_teams(self, db: Session):
        teams = crud.nfl_team.get_multi(db=db)
        return teams

    def add_team(self, db: Session, team: dict):
        nickname = ''
        if 'name' not in team:
            nickname = team['displayName']
        else:
            nickname = team['name']

        team_create = NFLTeamCreate(
            id=team['id'],
            abbreviation=team['abbreviation'],
            city_state=team['location'],
            full_name=team['displayName'],
            nickname=nickname
        )

        crud.nfl_team.create(db, obj_in=team_create)


nfl_team_service = NFLTeamService()


