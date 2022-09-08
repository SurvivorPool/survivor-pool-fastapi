from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import dependencies
from schemas.nfl_team import NFLTeamResponse
from services.game import game_service
from services.odds import odds_service
from services.stadium import stadium_service
from schemas.game import GameResponseFull, GameList

authorized_router = APIRouter(
    prefix='/games',
    tags=['games'],
    # dependencies=[Depends(dependencies.get_current_user)]
)


@authorized_router.get('', response_model=GameList)
async def games(db: Session = Depends(dependencies.get_db)):
    await game_service.update_games(db)
    week_num = game_service.get_max_week(db)
    game_models = game_service.get_games_by_week(db, week_num)

    game_responses = []
    for game_model in game_models:
        odds_model = odds_service.get_by_id(db, game_model.id)
        stadium_model = stadium_service.get_stadium_by_id(db, game_model.stadium_id)

        game_response = GameResponseFull(
            id=game_model.id,
            home_team_name=game_model.home_team_name,
            home_team_score=game_model.home_team_score,
            away_team_name=game_model.away_team_name,
            away_team_score=game_model.away_team_score,
            day_of_week=game_model.day_of_week,
            game_date=game_model.game_date,
            quarter=game_model.quarter,
            quarter_time=game_model.quarter_time,
            week=game_model.week,
            stadium_id=game_model.stadium_id,
            odds=odds_model,
            stadium=stadium_model,
            home_team_info=NFLTeamResponse(**game_model.home_team_info.__dict__),
            away_team_info=NFLTeamResponse(**game_model.away_team_info.__dict__),
        )

        game_responses.append(game_response)
    games_response = GameList(games=game_responses)
    return games_response


