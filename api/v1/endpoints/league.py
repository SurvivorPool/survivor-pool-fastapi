from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import dependencies
from schemas.league import LeagueCreate, LeagueUpdate, LeagueResponse, LeagueResponseFull, LeagueList
from services.league import league_service

authenticated_router = APIRouter(
    prefix="/leagues",
    tags=['leagues'],
    dependencies=[Depends(dependencies.get_current_user)]
)

admin_router = APIRouter(
    prefix='/admin/leagues',
    tags=['league administration'],
    dependencies=[Depends(dependencies.get_admin_user)]
)


@authenticated_router.get('/', response_model=LeagueList)
def get_leagues(db: Session = Depends(dependencies.get_db)):
    league_models = league_service.get_all(db)
    league_responses = []
    for league_model in league_models:
        league_response = LeagueResponse(**league_model.__dict__)
        league_responses.append(league_response)

    leagues_response = LeagueList(leagues=league_responses)

    return leagues_response


@admin_router.post('/', response_model=LeagueResponse)
def create_league(league_create_input: LeagueCreate, db: Session = Depends(dependencies.get_db)):
    try:
        league_model = league_service.create_league(db, league_create_input)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.args
        )

    league_response = LeagueResponse(**league_model.__dict__)

    return league_response


@admin_router.put('/', response_model=LeagueResponse)
def update_league(league_update_input: LeagueUpdate, db: Session = Depends(dependencies.get_db)):
    try:
        league_model = league_service.update_league(db, league_update_input)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.args
        )
    league_response = LeagueResponse(**league_model.__dict__)
    return league_response
