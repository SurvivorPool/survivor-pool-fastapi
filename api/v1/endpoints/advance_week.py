from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from sqlalchemy.orm import Session

from api import dependencies
from schemas.player_team import AdvanceWeekResponse, PlayerTeamResponse
from services.game import game_service
from services.league import league_service
from services.pick import pick_service
from services.player_team import player_team_service

admin_router = APIRouter(
    prefix="/admin/advance_week",
    tags=['admin advance week'],
    dependencies=[Depends(dependencies.get_admin_user)]
)


@admin_router.put('', response_model=AdvanceWeekResponse)
def advance_week(db: Session = Depends(dependencies.get_db)):
    # await game_service.update_games(db)

    week_num = game_service.get_max_week(db)
    game_models = game_service.get_games_by_week(db, week_num)

    for game_model in game_models:
        if game_model.quarter != "F" and game_model.quarter != "FO":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not all games have been completed")

    player_team_models = player_team_service.get_all(db)
    losers = game_service.get_losers_for_week(db, week_num)
    deactivated_teams = []
    advancing_teams = []

    for player_team_model in player_team_models:
        pick_model = pick_service.get_player_team_pick_for_week(db, player_team_model.id, week_num)
        if not pick_model:
            deactivated_team = player_team_service.deactivate_team(db, player_team_model)
            deactivated_teams.append(player_team_model)
        else:
            if pick_model and pick_model.nfl_team_name in losers:
                deactivated_team = player_team_service.deactivate_team(db, player_team_model)
                deactivated_teams.append(player_team_model)
            else:
                advancing_team = player_team_service.increase_streak(db, player_team_model)
                advancing_teams.append(player_team_model)

    advance_week_response = AdvanceWeekResponse(
        deactivated_teams=[PlayerTeamResponse(
            id=deactivated_team.id,
            league_id=deactivated_team.league_id,
            user_id=deactivated_team.user_id,
            name=deactivated_team.name,
            active=deactivated_team.active,
            paid=deactivated_team.paid,
            streak=deactivated_team.streak,
            current_pick=player_team_service.get_current_pick(db, deactivated_team.id),
        ) for deactivated_team in deactivated_teams],
        advancing_teams=[PlayerTeamResponse(
            id=advancing_team.id,
            league_id=advancing_team.league_id,
            user_id=advancing_team.user_id,
            name=advancing_team.name,
            active=advancing_team.active,
            paid=advancing_team.paid,
            streak=advancing_team.streak,
            current_pick=player_team_service.get_current_pick(db, advancing_team.id),
        ) for advancing_team in advancing_teams]
    )
    return advance_week_response













