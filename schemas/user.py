from pydantic import BaseModel, HttpUrl
from uuid import UUID


class UserBase(BaseModel):
    full_name: str
    email: str
    is_admin: bool
    picture_url: HttpUrl
    receive_notifications: bool
    provider: str
    wins: int


class UserExistsCheckResponse(BaseModel):
    exists: bool


class UserCreate(UserBase):
    ...


class UserUpdate(BaseModel):
    receive_notifications: bool


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: UUID

    class Config:
        orm_mode = True


# Properties to return to client
class UserResponse(UserInDBBase):
    ...
