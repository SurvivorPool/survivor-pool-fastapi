from crud.base import CRUDBase
from models.user_message import UserMessage
from schemas.user_message import UserMessageCreateDB, UserMessageUpdate


class UserMessageCRUD(CRUDBase[UserMessage, UserMessageCreateDB, UserMessageUpdate]):
    ...


user_message = UserMessageCRUD(UserMessage)
