from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import dependencies
from models.user import User
from schemas.league import LeagueResponse
from schemas.user import UserResponse
from services.player_team import player_team_service
from schemas.player_team import PlayerTeamCreate, PlayerTeamUpdate, PlayerTeamResponse, PlayerTeamResponseFull, PlayerTeamList

authorized_router = APIRouter(
    prefix="/player_teams",
    tags=["player teams"],
    dependencies=[Depends(dependencies.get_current_user)]
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
        league=LeagueResponse(**player_team_model.league.__dict__)
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
        league=LeagueResponse(**player_team_model.league.__dict__)
    )
    return player_team_response


@authorized_router.put('/{player_team_id}', response_model=PlayerTeamResponseFull)
def update_player_team(
        player_team_id: UUID,
        player_team_input: PlayerTeamUpdate,
        db: Session = Depends(dependencies.get_db),
        current_user: User = Depends(dependencies.get_current_user)
):
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
        league=LeagueResponse(**player_team_model.league.__dict__)
    )
    return player_team_response



