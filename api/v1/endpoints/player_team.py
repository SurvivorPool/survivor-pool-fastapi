from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import dependencies
from models.user import User
from schemas.common import DeleteModel
from schemas.league import LeagueResponse
from schemas.user import UserResponse
from services.league import league_service
from services.player_team import player_team_service
from schemas.player_team import AdminPlayerTeamUpdate, PlayerTeamCreate, PlayerTeamUpdate,PlayerTeamResponseFull, PlayerTeamList

authorized_router = APIRouter(
    prefix='/player_teams',
    tags=['player teams'],
    dependencies=[Depends(dependencies.get_current_user)]
)

admin_router = APIRouter(
    prefix='/admin/player_teams',
    tags=['player teams administration'],
    dependencies=[Depends(dependencies.get_admin_user)]
)


@authorized_router.get('/{player_team_id}')
def get_player_team(player_team_id: UUID,db: Session = Depends(dependencies.get_db)):
    player_team_model = player_team_service.get_by_id(db, player_team_id)

    if not player_team_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find player team")

    player_team_response = PlayerTeamResponseFull(
        id=player_team_model.id,
        league_id=player_team_model.league_id,
        user_id=player_team_model.user_id,
        name=player_team_model.name,
        active=player_team_model.active,
        paid=player_team_model.paid,
        streak=player_team_model.streak,
        user=UserResponse(**player_team_model.user.__dict__),
        current_pick=player_team_service.get_current_pick(db, player_team_model.id),
        league=LeagueResponse(
            id=player_team_model.league.id,
            name=player_team_model.league.name,
            description=player_team_model.league.description,
            price=player_team_model.league.price,
            start_week=player_team_model.league.start_week,
            completed=player_team_model.league.completed,
            type_id=player_team_model.league.type_id,
            pot=len(player_team_model.league.teams) * player_team_model.league.price,
            signup_active=(not league_service.has_league_started(db, player_team_model.league_id))
        )
    )
    return player_team_response


@authorized_router.post("/", response_model=PlayerTeamResponseFull)
def create_player_team(
        player_team_input: PlayerTeamCreate,
        db: Session = Depends(dependencies.get_db),
        current_user: User = Depends(dependencies.get_current_user)
):
    player_team_model = player_team_service.create_player_team(db, player_team_input, current_user)
    player_team_response = PlayerTeamResponseFull(
        id=player_team_model.id,
        league_id=player_team_model.league_id,
        user_id=player_team_model.user_id,
        name=player_team_model.name,
        active=player_team_model.active,
        paid=player_team_model.paid,
        streak=player_team_model.streak,
        user=UserResponse(**player_team_model.user.__dict__),
        current_pick=player_team_service.get_current_pick(db, player_team_model.id),
        league=LeagueResponse(
            id=player_team_model.league.id,
            name=player_team_model.league.name,
            description=player_team_model.league.description,
            price=player_team_model.league.price,
            start_week=player_team_model.league.start_week,
            completed=player_team_model.league.completed,
            type_id=player_team_model.league.type_id,
            pot=len(player_team_model.league.teams) * player_team_model.league.price,
            signup_active=(not league_service.has_league_started(db, player_team_model.league_id))
        )
    )
    return player_team_response


@authorized_router.put('/{player_team_id}', response_model=PlayerTeamResponseFull)
def update_player_team(
        player_team_id: UUID,
        player_team_input: PlayerTeamUpdate,
        db: Session = Depends(dependencies.get_db),
        current_user: User = Depends(dependencies.get_current_user)
):
    player_team_check = player_team_service.get_by_id(db, player_team_id)
    if player_team_check.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update another user's team")

    player_team_model = player_team_service.update_player_team(db, player_team_id, player_team_input, current_user)
    player_team_response = PlayerTeamResponseFull(
        id=player_team_model.id,
        league_id=player_team_model.league_id,
        user_id=player_team_model.user_id,
        name=player_team_model.name,
        active=player_team_model.active,
        paid=player_team_model.paid,
        streak=player_team_model.streak,
        user=UserResponse(**player_team_model.user.__dict__),
        current_pick=player_team_service.get_current_pick(db, player_team_model.id),
        league=LeagueResponse(
            id=player_team_model.league.id,
            name=player_team_model.league.name,
            description=player_team_model.league.description,
            price=player_team_model.league.price,
            start_week=player_team_model.league.start_week,
            completed=player_team_model.league.completed,
            type_id=player_team_model.league.type_id,
            pot=len(player_team_model.league.teams) * player_team_model.league.price,
            signup_active=(not league_service.has_league_started(db, player_team_model.league_id))
        )
    )
    return player_team_response


@admin_router.get('/', response_model=PlayerTeamList)
def admin_get_all_player_teams(db: Session = Depends(dependencies.get_db)):
    player_team_models = player_team_service.get_all(db)
    player_team_responses = []
    for player_team_model in player_team_models:
        player_team_response = PlayerTeamResponseFull(
                id=player_team_model.id,
                league_id=player_team_model.league_id,
                user_id=player_team_model.user_id,
                name=player_team_model.name,
                active=player_team_model.active,
                paid=player_team_model.paid,
                streak=player_team_model.streak,
                current_pick=player_team_service.get_current_pick(db, player_team_model.id),
                user=UserResponse(**player_team_model.user.__dict__),
                league=LeagueResponse(id=player_team_model.league.id,
                        name=player_team_model.league.name,
                        description=player_team_model.league.description,
                        price=player_team_model.league.price,
                        start_week=player_team_model.league.start_week,
                        completed=player_team_model.league.completed,
                        type_id=player_team_model.league.type_id,
                        pot=len(player_team_model.league.teams) * player_team_model.league.price,
                        signup_active=(not league_service.has_league_started(db, player_team_model.league_id)))
            )
        player_team_responses.append(player_team_response)

    player_teams_response = PlayerTeamList(teams=player_team_responses)
    return player_teams_response


@admin_router.put('/{player_team_id}', response_model=PlayerTeamResponseFull)
def admin_update_player_team(
        player_team_id: UUID,
        admin_player_team_update: AdminPlayerTeamUpdate,
        db: Session = Depends(dependencies.get_db),
        current_user = Depends(dependencies.get_admin_user)
):
    player_team_model = player_team_service.update_player_team(
        db,
        player_team_id,
        admin_player_team_update,
        current_user
    )
    
    player_team_response = PlayerTeamResponseFull(
        id=player_team_model.id,
        league_id=player_team_model.league_id,
        user_id=player_team_model.user_id,
        name=player_team_model.name,
        active=player_team_model.active,
        paid=player_team_model.paid,
        streak=player_team_model.streak,
        current_pick=player_team_service.get_current_pick(db, player_team_model.id),
        user=UserResponse(**player_team_model.user.__dict__),
        league=LeagueResponse(
            id=player_team_model.league.id,
            name=player_team_model.league.name,
            description=player_team_model.league.description,
            price=player_team_model.league.price,
            start_week=player_team_model.league.start_week,
            completed=player_team_model.league.completed,
            type_id=player_team_model.league.type_id,
            pot=len(player_team_model.league.teams) * player_team_model.league.price,
            signup_active=(not league_service.has_league_started(db, player_team_model.league_id))
        )
    )
    return player_team_response


@admin_router.delete("/{player_team_id}", response_model=DeleteModel)
def admin_delete_player_team(player_team_id: UUID, db: Session = Depends(dependencies.get_db)):
    player_team_model = player_team_service.delete(db, player_team_id)
    return DeleteModel(success=True, detail="Player team successfully deleted")





