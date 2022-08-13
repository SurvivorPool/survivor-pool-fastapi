from pydantic import BaseModel
from uuid import UUID


class StadiumBase(BaseModel):
    city: str
    name: str
    state: str
    roof_type: str


class StadiumCreate(StadiumBase):
    ...


class StadiumUpdate(StadiumBase):
    ...


class StadiumInDBBase(StadiumBase):
    id: UUID

    class Config:
        orm_mode = True


class StadiumResponse(StadiumInDBBase):
    ...