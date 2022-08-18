from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import dependencies
from models import PlayerTeam, League
from schemas.league import LeagueCreate, LeagueUpdate, LeagueResponse, LeagueList
from schemas.league_full import LeagueResponseFull
from schemas.league_type import LeagueTypeResponse
from schemas.player_team import PlayerTeamResponse
from services.league import league_service
from services.player_team import player_team_service

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


@authenticated_router.get('/{league_id}')
def get_league(league_id: UUID, db: Session = Depends(dependencies.get_db)):
    league_model = league_service.get_by_id(db, league_id)
    league_response = LeagueResponseFull(
        id=league_model.id,
        name=league_model.name,
        description=league_model.description,
        price=league_model.price,
        start_week=league_model.start_week,
        completed=league_model.completed,
        type_id=league_model.type_id,
        league_type=LeagueTypeResponse(**league_model.league_type.__dict__),
        teams=[PlayerTeamResponse(**player_team.__dict__) for player_team in league_model.teams]
    )

    return league_response


@admin_router.post('/', response_model=LeagueResponseFull)
def create_league(league_create_input: LeagueCreate, db: Session = Depends(dependencies.get_db)):
    try:
        league_model = league_service.create_league(db, league_create_input)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.args
        )

    league_response = LeagueResponseFull(
        id=league_model.id,
        name=league_model.name,
        description=league_model.description,
        price=league_model.price,
        start_week=league_model.start_week,
        completed=league_model.completed,
        type_id=league_model.type_id,
        league_type=LeagueTypeResponse(**league_model.league_type.__dict__),
        teams=[]
    )

    return league_response


@admin_router.put('/', response_model=LeagueResponseFull)
def update_league(league_update_input: LeagueUpdate, db: Session = Depends(dependencies.get_db)):
    try:
        league_model = league_service.update_league(db, league_update_input)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.args
        )
    league_response = LeagueResponseFull(
            id=league_model.id,
            name=league_model.name,
            description=league_model.description,
            price=league_model.price,
            start_week=league_model.start_week,
            completed=league_model.completed,
            type_id=league_model.type_id,
            league_type=LeagueTypeResponse(**league_model.league_type.__dict__),
            teams=[PlayerTeamResponse(**player_team.__dict__) for player_team in league_model.teams]
        )
    return league_response
