from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

from schemas.message_type import MessageTypeResponse
from schemas.user import UserResponse


class UserMessageBase(BaseModel):
    text: str
    type_id: UUID
    user_id: str


class UserMessageCreate(BaseModel):
    text: str
    type_id: UUID
    user_ids: list[UUID]
    all_users: bool


class UserMessageCreateDB(UserMessageBase):
    ...


class UserMessageUpdate(BaseModel):
    read: bool
    read_date: Optional[datetime]


class UserMessageInDBBase(UserMessageBase):
    id: UUID
    created_date: datetime
    read: bool
    read_date: Optional[datetime]

    class Config:
        orm_mode = True


class UserMessageResponse(UserMessageInDBBase):
    ...


class UserMessageResponseFull(UserMessageResponse):
    message_type: MessageTypeResponse
    user: UserResponse


class UserMessageList(BaseModel):
    messages: list[UserMessageResponseFull]

