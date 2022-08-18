from pydantic import BaseModel


class StadiumBase(BaseModel):
    id: int
    city: str
    name: str
    state: str


class StadiumCreate(StadiumBase):
    ...


class StadiumUpdate(StadiumBase):
    ...


class StadiumInDBBase(StadiumBase):
    class Config:
        orm_mode = True


class StadiumResponse(StadiumInDBBase):
    ...


class StadiumList(BaseModel):
    stadiums: list[StadiumResponse]