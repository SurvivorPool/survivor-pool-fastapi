from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import dependencies
from schemas.league import LeagueCreate, LeagueUpdate, LeagueResponse
from schemas.league_full import LeagueResponseFull, LeagueListFull
from schemas.league_type import LeagueTypeResponse
from schemas.player_team import PlayerTeamResponseFull
from schemas.user import UserResponse
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


@authenticated_router.get('', response_model=LeagueListFull)
def get_leagues(db: Session = Depends(dependencies.get_db)):
    league_models = league_service.get_all(db)
    league_responses = []
    for league_model in league_models:
        league_response = LeagueResponseFull(
            id=league_model.id,
            name=league_model.name,
            description=league_model.description,
            price="{:,.2f}".format(league_model.price),
            start_week=league_model.start_week,
            completed=league_model.completed,
            type_id=league_model.type_id,
            pot=len(league_model.teams) * league_model.price,
            signup_active=(not league_service.has_league_started(db, league_model.id)),
            league_type=LeagueTypeResponse(**league_model.league_type.__dict__),
            teams=[
                PlayerTeamResponseFull(
                    id=player_team.id,
                    league_id=player_team.league_id,
                    user_id=player_team.user_id,
                    name=player_team.name,
                    active=player_team.active,
                    paid=player_team.paid,
                    streak=player_team.streak,
                    current_pick=player_team_service.get_current_pick(db, player_team.id),
                    user=UserResponse(**player_team.user.__dict__),
                    league=LeagueResponse(
                        id=player_team.league.id,
                        name=player_team.league.name,
                        description=player_team.league.description,
                        price=player_team.league.price,
                        start_week=player_team.league.start_week,
                        completed=player_team.league.completed,
                        type_id=player_team.league.type_id,
                        pot=len(player_team.league.teams) * player_team.league.price,
                        signup_active=(not league_service.has_league_started(db, player_team.league_id))
                    )
            )
                for player_team in league_model.teams]
        )
        league_responses.append(league_response)

    leagues_response = LeagueListFull(leagues=league_responses)

    return leagues_response


@authenticated_router.get('/user/{user_id}', response_model=LeagueListFull)
def get_leagues_for_user(user_id: str, db: Session = Depends(dependencies.get_db)):
    player_teams = player_team_service.get_by_user_id(db, user_id)

    league_responses = []
    for player_team in player_teams:
        league_model = player_team.league
        league_response = LeagueResponseFull(
            id=league_model.id,
            name=league_model.name,
            description=league_model.description,
            price=league_model.price,
            start_week=league_model.start_week,
            completed=league_model.completed,
            type_id=league_model.type_id,
            pot=len(league_model.teams) * league_model.price,
            signup_active=(not league_service.has_league_started(db, league_model.id)),
            league_type=LeagueTypeResponse(**league_model.league_type.__dict__),
            teams=[PlayerTeamResponseFull(
            id=player_team.id,
            league_id=player_team.league_id,
            user_id=player_team.user_id,
            name=player_team.name,
            active=player_team.active,
            paid=player_team.paid,
            streak=player_team.streak,
            current_pick=player_team_service.get_current_pick(db, player_team.id),
            user=UserResponse(**player_team.user.__dict__),
            league=LeagueResponse(
                id=player_team.league.id,
                name=player_team.league.name,
                description=player_team.league.description,
                price=player_team.league.price,
                start_week=player_team.league.start_week,
                completed=player_team.league.completed,
                type_id=player_team.league.type_id,
                pot=len(player_team.league.teams) * player_team.league.price,
                signup_active=(not league_service.has_league_started(db, player_team.league_id)))
            ) for player_team in league_model.teams]
        )
        league_responses.append(league_response)

    leagues_response = LeagueListFull(leagues=league_responses)

    return leagues_response


@authenticated_router.get('/{league_id}')
def get_league(league_id: UUID, db: Session = Depends(dependencies.get_db)):
    league_model = league_service.get_by_id(db, league_id)

    if not league_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find league with that id")

    league_response = LeagueResponseFull(
        id=league_model.id,
        name=league_model.name,
        description=league_model.description,
        price=league_model.price,
        start_week=league_model.start_week,
        completed=league_model.completed,
        type_id=league_model.type_id,
        pot=len(league_model.teams) * league_model.price,
        signup_active=(not league_service.has_league_started(db, league_model.id)),
        league_type=LeagueTypeResponse(**league_model.league_type.__dict__),
        teams=[PlayerTeamResponseFull(
            id=player_team.id,
            league_id=player_team.league_id,
            user_id=player_team.user_id,
            name=player_team.name,
            active=player_team.active,
            paid=player_team.paid,
            streak=player_team.streak,
            user=UserResponse(**player_team.user.__dict__),
            current_pick=player_team_service.get_current_pick(db, player_team.id),
            league=LeagueResponse(
                id=player_team.league.id,
                name=player_team.league.name,
                description=player_team.league.description,
                price=player_team.league.price,
                start_week=player_team.league.start_week,
                completed=player_team.league.completed,
                type_id=player_team.league.type_id,
                pot=len(player_team.league.teams) * player_team.league.price,
                signup_active=(not league_service.has_league_started(db, player_team.league_id)))
            ) for player_team in league_model.teams]
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
        pot=len(league_model.teams) * league_model.price,
        signup_active=(not league_service.has_league_started(db, league_model.id)),
        league_type=LeagueTypeResponse(**league_model.league_type.__dict__),
        teams=[PlayerTeamResponseFull(
            id=player_team.id,
            league_id=player_team.league_id,
            user_id=player_team.user_id,
            name=player_team.name,
            active=player_team.active,
            paid=player_team.paid,
            streak=player_team.streak,
            user=UserResponse(**player_team.user.__dict__),
            current_pick=player_team_service.get_current_pick(db, player_team.id),
            league=LeagueResponse(
                id=player_team.league.id,
                name=player_team.league.name,
                description=player_team.league.description,
                price=player_team.league.price,
                start_week=player_team.league.start_week,
                completed=player_team.league.completed,
                type_id=player_team.league.type_id,
                pot=len(player_team.league.teams) * player_team.league.price,
                signup_active=(not league_service.has_league_started(db, player_team.league_id))
            )
        ) for player_team in league_model.teams]
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
            pot=len(league_model.teams) * league_model.price,
            signup_active=(not league_service.has_league_started(db, league_model.id)),
            league_type=LeagueTypeResponse(**league_model.league_type.__dict__),
            teams=[PlayerTeamResponseFull(
            id=player_team.id,
            league_id=player_team.league_id,
            user_id=player_team.user_id,
            name=player_team.name,
            active=player_team.active,
            paid=player_team.paid,
            streak=player_team.streak,
            current_pick=player_team_service.get_current_pick(db, player_team.id),
            user=UserResponse(**player_team.user.__dict__),
            league=LeagueResponse(
                id=player_team.league.id,
                name=player_team.league.name,
                description=player_team.league.description,
                price=player_team.league.price,
                start_week=player_team.league.start_week,
                completed=player_team.league.completed,
                type_id=player_team.league.type_id,
                pot=len(player_team.league.teams) * player_team.league.price,
                signup_active=(not league_service.has_league_started(db, player_team.league_id)))
            ) for player_team in league_model.teams]
        )
    return league_response
