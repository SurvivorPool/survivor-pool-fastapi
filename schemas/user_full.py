from pydantic import BaseModel
from schemas.player_team import PlayerTeamResponse
from schemas.user import UserInDBBase


class UserResponseFull(UserInDBBase):
    teams: list[PlayerTeamResponse]


class UsersListFull(BaseModel):
    users: list[UserResponseFull]