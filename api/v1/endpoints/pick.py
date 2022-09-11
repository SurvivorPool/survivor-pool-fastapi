from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from models import User
from api import dependencies
from schemas.game import GameResponse
from schemas.nfl_team import NFLTeamResponse
from schemas.pick import PickUpdate
from schemas.pick_full import PickResponseFull
from schemas.player_team import PlayerTeamResponse
from services.game import game_service
from services.nfl_team import nfl_team_service
from services.pick import pick_service
from services.player_team import player_team_service

authorized_router = APIRouter(
    prefix="/picks",
    tags=['picks']
)


@authorized_router.put('', response_model=PickResponseFull)
async def make_pick(
        pick_upsert_input: PickUpdate,
        db: Session = Depends(dependencies.get_db),
        current_user: User = Depends(dependencies.get_current_user)
):
    user_player_team_ids = [player_team.id for player_team in current_user.teams]
    if not (pick_upsert_input.player_team_id in user_player_team_ids):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            details="Cannot update another user's team's pick"
        )

    player_team_model = player_team_service.get_by_id(db, pick_upsert_input.player_team_id)

    if not player_team_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find a player team with that id"
        )

    if not player_team_model.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot make pick for inactive player team"
        )

    await game_service.update_games(db)
    game_model = game_service.get_by_id(db, pick_upsert_input.game_id)

    if not game_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find a player team with that id"
        )

    if game_model.quarter != "P":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot pick a game that has already started"
        )

    nfl_team_model = nfl_team_service.get_team_by_nickname(db, pick_upsert_input.nfl_team_name)

    if not nfl_team_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NFL Team not found"
        )

    if pick_upsert_input.nfl_team_name not in [game_model.home_team_name, game_model.away_team_name]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Selected nfl team is not playing in the selected game"
        )
    current_week = game_service.get_max_week(db)
    already_picked_team_names = [pick.nfl_team_name for pick in player_team_model.picks if pick.week_num != current_week ]

    if pick_upsert_input.nfl_team_name in already_picked_team_names:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot pick the same team twice"
        )

    pick_model = pick_service.make_pick(db, player_team_model.id, game_model.id, nfl_team_model.nickname)

    pick_response = PickResponseFull(
        id=pick_model.id,
        nfl_team_name=pick_model.nfl_team_name,
        game_id=pick_model.game_id,
        week_num=pick_model.week_num,
        player_team_id=pick_model.player_team_id,
        player_team=PlayerTeamResponse(
                id=pick_model.player_team.id,
                league_id=pick_model.player_team.league_id,
                user_id=pick_model.player_team.user_id,
                name=pick_model.player_team.name,
                active=pick_model.player_team.active,
                paid=pick_model.player_team.paid,
                streak=pick_model.player_team.streak,
                current_pick=player_team_service.get_current_pick(db, pick_model.player_team.id)
            ),
        nfl_team_info=NFLTeamResponse(**pick_model.nfl_team_info.__dict__),
        game=GameResponse(**pick_model.game.__dict__)
    )
    return pick_response








