from pydantic import BaseModel
from typing import Optional


class NFLTeamBase(BaseModel):
    id: int
    abbreviation: str
    city_state: str
    full_name: str
    nickname: str
    conference: Optional[str]
    division: Optional[str]


class NFLTeamCreate(NFLTeamBase):
    ...


class NFLTeamUpdate(NFLTeamBase):
    ...


class NFLTeamInDBBase(NFLTeamBase):
    class Config:
        orm_mode = True


class NFLTeamResponse(NFLTeamInDBBase):
    ...


class NFLTeamList(BaseModel):
    nfl_teams: list[NFLTeamResponse]