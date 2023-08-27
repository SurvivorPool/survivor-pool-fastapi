from pydantic import BaseModel
from uuid import UUID


class AdminMessageBase(BaseModel):
    user_id: str
    message: str
    show: bool
    type: str


class AdminMessageCreate(AdminMessageBase):
    ...


class AdminMessageUpdate(AdminMessageBase):
    id: UUID


class AdminMessageInDBBase(AdminMessageBase):
    id: UUID

    class Config:
        from_attributes = True


class AdminMessageResponse(AdminMessageInDBBase):
    ...


class AdminMessageResponseList(BaseModel):
    messages: list[AdminMessageResponse]

