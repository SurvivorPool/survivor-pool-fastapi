from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import dependencies
from schemas.league_type import LeagueTypeCreate, LeagueTypeUpdate, LeagueTypeResponse, LeagueTypeList
from services.league_type_service import league_type_service

admin_router = APIRouter(
    prefix='/admin/league_types',
    tags=['league administration'],
    dependencies=[Depends(dependencies.get_admin_user)]
)


@admin_router.get('/', response_model=LeagueTypeList)
def league_types(db: Session = Depends(dependencies.get_db)):
    league_type_models = league_type_service.get_all(db)
    league_types_responses = []
    for league_type in league_type_models:
        league_type_response = LeagueTypeResponse(**league_type.__dict__)
        league_types_responses.append(league_type_response)
    league_types_response = LeagueTypeList(league_types=league_types_responses)
    return league_types_response


@admin_router.post('/', response_model=LeagueTypeResponse)
def create_league_type(league_type_create: LeagueTypeCreate, db: Session = Depends(dependencies.get_db)):
    league_type_model = league_type_service.get_by_name(db, league_type_create.name)

    if league_type_model is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='League Type with that name already exists',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    league_type_model = league_type_service.create_league_type(db, league_type_create)

    league_type_response = LeagueTypeResponse(**league_type_model.__dict__)
    return league_type_response


