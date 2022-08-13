from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import dependencies
from services.stadium import stadium_service
from schemas.stadium import StadiumResponse, StadiumList

authorized_router = APIRouter(
    prefix='/stadiums',
    tags=['stadiums'],
    dependencies=[Depends(dependencies.get_current_user)]
)


@authorized_router.get('/', response_model=StadiumList)
async def stadiums(db: Session = Depends(dependencies.get_db)):
    stadium_models = stadium_service.get_stadiums(db)
    response_stadiums = []
    for stadium in stadium_models:
        response_stadium = StadiumResponse(
            **stadium.__dict__
        )
        response_stadiums.append(response_stadium)
    response = StadiumList(stadiums=response_stadiums)
    return response
