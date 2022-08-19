from crud.base import CRUDBase
from models.admin_message import AdminMessage
from schemas.admin_message import AdminMessageCreate, AdminMessageUpdate


class CRUDAdminMessage(CRUDBase[AdminMessage, AdminMessageCreate, AdminMessageUpdate]):
    ...


admin_message = CRUDAdminMessage(AdminMessage)
# ading a comment




