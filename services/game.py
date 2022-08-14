import httpx
import calendar
import crud
from datetime import timedelta
from dateutil import parser
from sqlalchemy.orm import Session
from schemas.game import GameCreate, GameUpdate
from schemas.odds import OddsCreate, OddsUpdate
from services.stadium import stadium_service
from services.nfl_team import nfl_team_service


class GameService:
    nfl_endpoint = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

    async def update_games(self, db: Session):
        rss_feed = httpx.get(self.nfl_endpoint)
        await nfl_team_service.update_nfl_teams(db, rss_feed)
        await stadium_service.update_stadiums(db, rss_feed)

        json = rss_feed.json()
        week_info = json['week']
        week_num = week_info['number']

        events = json['events']

        for event in events:
            competitions = event['competitions']
            competition = competitions[0]
            teams = competition['competitors']

            home_team = next(filter(lambda team: team['homeAway'] == 'home', teams))
            away_team = next(filter(lambda team: team['homeAway'] == 'away', teams))
            status = event['status']
            game_type = status['type']

            game_id = event['id']
            game_model = crud.game.get(db, game_id)

            home_team_score = home_team['score'] or 0
            away_team_score = away_team['score'] or 0

            if status['period'] == 0 and game_type['state'] == 'pre':
                quarter = 'P'
            elif game_type['state'] == 'post':
                quarter = 'F'
            else:
                quarter = status['period']

            quarter_time = status['displayClock']
            game_date = parser.parse(competition['startDate'])
            game_date_eastern = game_date - timedelta(hours=5)
            day_of_week = calendar.day_name[game_date_eastern.weekday()]
            stadium_id = competition['venue']['id']

            if game_model is None:
                if 'name' not in home_team['team']:
                    home_team_name = home_team['team']['displayName']
                else:
                    home_team_name = home_team['team']['name']

                if 'name' not in away_team['team']:
                    away_team_name = away_team['team']['displayName']
                else:
                    away_team_name = away_team['team']['name']

                game_create = GameCreate(
                    id=game_id,
                    home_team_name=home_team_name,
                    home_team_score=home_team_score,
                    away_team_name=away_team_name,
                    away_team_score=away_team_score,
                    day_of_week=day_of_week,
                    game_date=game_date,
                    quarter=quarter,
                    quarter_time=quarter_time,
                    week=week_num,
                    stadium_id=stadium_id
                )
                crud.game.create(db=db, obj_in=game_create)
            else:
                game_update = GameUpdate(
                    id=game_id,
                    home_team_score=home_team_score,
                    away_team_score=away_team_score,
                    quarter=quarter,
                    quarter_time=quarter_time,
                    game_date=game_date,
                    day_of_week=day_of_week,
                    stadium_id=stadium_id
                )
                crud.game.update(db, db_obj=game_model, obj_in=game_update)

            if 'odds' in competition:
                odds = competition['odds']

                if odds:
                    odds_model = crud.odds.get(db, game_id)

                    if odds_model is None:
                        if 'details' in odds[0] and 'overUnder' in odds[0]:
                            odds_create = OddsCreate(
                                id=game_id,
                                details=odds[0]['details'],
                                over_under=odds[0]['overUnder']
                            )
                            crud.odds.create(db, obj_in=odds_create)
                    else:
                        odds_update = OddsUpdate(
                            id=odds_model.id,
                            details=odds[0]['details'],
                            over_under=odds[0]['overUnder']
                        )
                        crud.odds.update(db, db_obj=odds_model, obj_in=odds_update)

    def get_games(self, db: Session):
        return crud.game.get_multi(db=db)












game_service = GameService()
