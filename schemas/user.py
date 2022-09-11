from pydantic import BaseModel, HttpUrl
from uuid import UUID


class UserBase(BaseModel):
    full_name: str
    email: str
    is_admin: bool
    picture_url: HttpUrl
    receive_notifications: bool
    wins: int


class UserExistsCheckResponse(BaseModel):
    exists: bool


class UserCreate(BaseModel):
    id: str
    email: str
    full_name: str
    picture_url: str
    receive_notifications: bool



class UserUpdate(BaseModel):
    receive_notifications: bool


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: str

    class Config:
        orm_mode = True


# Properties to return to client
class UserResponse(UserInDBBase):
    ...
