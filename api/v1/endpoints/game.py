from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import dependencies
from services.game import game_service
from services.odds import odds
from schemas.game import GameResponse, GameList
from schemas.odds import OddsResponse

authorized_router = APIRouter(
    prefix='/games',
    tags=['games'],
    dependencies=[Depends(dependencies.get_current_user)]
)


@authorized_router.get('/')
async def games(db: Session = Depends(dependencies.get_db)):
    await game_service.update_games(db)
    game_models = game_service.get_games(db)

    game_responses = []
    for game in game_models:
        game_response = GameResponse(**game.__dict__)
        odds_model = odds.get_by_id(db, game.id)
        if odds_model:
            game_response.odds = OddsResponse(**odds_model.__dict__)

        game_responses.append(game_response)
    games_response = GameList(games=game_responses)
    return games_response


