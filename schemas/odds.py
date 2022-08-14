from pydantic import BaseModel
from typing import List


class OddsBase(BaseModel):
    id: int
    details: str
    over_under: float


class OddsCreate(OddsBase):
    ...


class OddsUpdate(OddsBase):
    ...


class OddsInDBBase(OddsBase):
    id: int
    class Config:
        orm_mode = True


class OddsResponse(OddsInDBBase):
    ...


class OddsList(BaseModel):
    odds: List[OddsResponse]


