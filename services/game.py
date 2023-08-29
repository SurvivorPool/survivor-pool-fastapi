import httpx
import calendar
import crud
from datetime import timedelta
from dateutil import parser
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models.game import Game
from schemas.game import GameCreate, GameUpdate
from schemas.odds import OddsCreate, OddsUpdate
from services.stadium import stadium_service
from services.nfl_team import nfl_team_service


class GameService:
    nfl_endpoint = 'https://site.api.espn.com/apis/v2/scoreboard/header?sport=football&league=nfl&lang=en&region=us&contentorigin=espn&tz=America%2FNew_York'

    def get_by_id(self, db, game_id: int) -> Game:
        return crud.game.get(db, game_id)


    async def update_games(self, db: Session):
        rss_feed = httpx.get(self.nfl_endpoint)
        json = rss_feed.json()['sports'][0]['leagues'][0]
        await nfl_team_service.update_nfl_teams(db, rss_feed)

        events = json['events']

        for event in events:
            teams = event['competitors']
            week_num = event['week']

            print(teams)
            home_team = next(filter(lambda team: team['homeAway'] == 'home', teams))
            print(home_team)
            away_team = next(filter(lambda team: team['homeAway'] == 'away', teams))
            status = event['fullStatus']
            game_type = status['type']

            game_id = event['id']
            game_model = crud.game.get(db, game_id)

            home_team_score = home_team['score'] or 0
            away_team_score = away_team['score'] or 0

            if game_type['state'] == 'pre':
                quarter = 'P'
            elif game_type['state'] == 'post':
                quarter = 'F'
            else:
                quarter = status['period']

            quarter_time = status['displayClock']
            game_date = parser.parse(event['date'])
            game_date_eastern = game_date - timedelta(hours=5)
            day_of_week = calendar.day_name[game_date_eastern.weekday()]

            if game_model is None:
                if 'name' not in home_team:
                    home_team_name = home_team['displayName']
                else:
                    home_team_name = home_team['name']

                if 'name' not in away_team:
                    away_team_name = away_team['displayName']
                else:
                    away_team_name = away_team['name']

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
                )
                crud.game.update(db, db_obj=game_model, obj_in=game_update)

            if event['odds'] is not None:
                odds = event['odds']

                odds_model = crud.odds.get(db, game_id)

                if odds_model is None:
                    if 'details' in odds and 'overUnder' in odds:
                        odds_create = OddsCreate(
                            id=game_id,
                            details=odds['details'],
                            over_under=odds['overUnder']
                        )
                        crud.odds.create(db, obj_in=odds_create)
                else:
                    odds_update = OddsUpdate(
                        id=odds_model.id,
                        details=odds['details'],
                        over_under=odds['overUnder']
                    )
                    crud.odds.update(db, db_obj=odds_model, obj_in=odds_update)

    def get_games(self, db: Session) -> list[Game]:
        return crud.game.get_multi(db=db)

    def get_games_by_week(self, db: Session, week_num: int) -> list[Game]:
        return crud.game.get_games_by_week(db, week_num)

    def get_max_week(self, db: Session) -> int:
        max_week = db.query(func.max(Game.week)).scalar()
        if not max_week:
            max_week = 1

        return max_week

    def get_losers_for_week(self, db:Session, week_num: int) -> list[str]:
        return crud.game.get_losers_for_week(db, week_num)













game_service = GameService()
