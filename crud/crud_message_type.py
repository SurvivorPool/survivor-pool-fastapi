from crud.base import CRUDBase
from models.message_type import MessageType
from schemas.message_type import MessageTypeCreate, MessageTypeUpdate


class CRUDMessageType(CRUDBase[MessageType, MessageTypeCreate, MessageTypeUpdate]):
    ...


message_type = CRUDMessageType(MessageType)
