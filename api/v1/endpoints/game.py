from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import dependencies
from services.game import game_service

authorized_router = APIRouter(
    prefix="/games",
    tags=["games"],
    dependencies=[Depends(dependencies.get_current_user)]
)


@authorized_router.get('/')
async def games(db: Session = Depends(dependencies.get_db)):
    await game_service.update_games(db)
    return {"test": "test"}


