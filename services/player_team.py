from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from models.user import User
from schemas.player_team import PlayerTeamCreate, PlayerTeamUpdate
import crud


class PlayerTeamService:
    def get_all(self, db):
        return crud.player_team.get_multi(db)

    def get_player_teams_by_league_id(self, db: Session, league_id: UUID):
        return crud.player_team.get_by_league_id(db, league_id)

    def get_by_id(self, db: Session, player_team_id: UUID):
        return crud.player_team.get(db, player_team_id)

    def get_by_user_id(self, db: Session, user_id: UUID):
        return crud.player_team.get_by_user_id(db, user_id)

    def create_player_team(self, db: Session, player_team_input: PlayerTeamCreate, current_user: User):
        league_model = crud.league.get(db, player_team_input.league_id)
        if not league_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="League not found")

        user_model = crud.user.get(db, player_team_input.user_id)
        if not user_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user_model.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create team for another user")

        player_team_model = crud.player_team.create(db, obj_in=player_team_input)
        return player_team_model

    def update_player_team(self, db: Session, player_team_id: UUID, player_team_input: PlayerTeamUpdate, current_user: User):
        player_team_model = crud.player_team.get(db, player_team_id)
        if not player_team_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player team not found")

        if player_team_model.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update team for another user")

        player_team_update_model = crud.player_team.update(db, db_obj=player_team_model, obj_in=player_team_input)
        return player_team_update_model

    def delete(self, db: Session, player_team_id: UUID):
        player_team_model = self.get_by_id(db, player_team_id)

        if not player_team_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player team not found")

        player_team_model = crud.player_team.remove(db, id=player_team_id)
        return player_team_model





player_team_service = PlayerTeamService()