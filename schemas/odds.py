from pydantic import BaseModel


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
        from_attributes = True


class OddsResponse(OddsInDBBase):
    ...


class OddsList(BaseModel):
    odds: list[OddsResponse]


