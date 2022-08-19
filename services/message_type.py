from uuid import UUID
from sqlalchemy.orm import Session
import crud
from schemas.message_type import MessageTypeCreate, MessageTypeUpdate


class MessageTypeService:
    def get_all(self, db: Session):
        return crud.message_type.get_multi(db)

    def create(self, db: Session, message_type_create_input: MessageTypeCreate):
        return crud.message_type.create(db=db, obj_in=message_type_create_input)

    def update(self, db: Session, message_type_id: UUID, message_type_update_input: MessageTypeUpdate):
        message_type_model = crud.message_type.get(db=db, id=message_type_id)
        return crud.message_type.update(db=db, db_obj=message_type_model, obj_in=message_type_update_input)


message_type_service = MessageTypeService()
