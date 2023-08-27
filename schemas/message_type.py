from pydantic import BaseModel
from uuid import UUID


class MessageTypeBase(BaseModel):
    name: str


class MessageTypeCreate(MessageTypeBase):
    ...


class MessageTypeUpdate(MessageTypeBase):
    ...


class MessageTypeInDBBase(MessageTypeBase):
    id: UUID

    class Config:
        from_attributes = True


class MessageTypeResponse(MessageTypeBase):
    id: UUID


class MessageTypeList(BaseModel):
    message_types: list[MessageTypeResponse]

