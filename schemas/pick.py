from pydantic import BaseModel
from uuid import UUID

class PickBase(BaseModel):
    player_team_id: UUID
    game_id: int
    nfl_team_name: str


class PickCreate(PickBase):
    week_num: int


class PickUpdate(PickBase):
    ...


class PickInDBBase(PickBase):
    id: UUID


class PickResponse(PickInDBBase):
    ...
