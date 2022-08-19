from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from models.user_message import UserMessage
from schemas.user_message import UserMessageCreateDB, UserMessageUpdate
import crud


class UserMessageService:
    def get_all(self, db: Session):
        return crud.user_message.get_multi(db=db)

    def get_by_id(self, db: Session, message_id: UUID):
        return crud.user_message.get(db=db, id=message_id)

    def get_unread_for_user_id(self, db: Session, user_id: UUID):
        unread_message_models = db.query(UserMessage).filter_by(read=False)
        return unread_message_models

    def create_message(self, db: Session, message_create_input: UserMessageCreateDB):
        return crud.user_message.create(db=db, obj_in=message_create_input)

    def update_message(self, db: Session, message_id: UUID, message_update_input: UserMessageUpdate):
        message_model = crud.user_message.get(db=db, id=message_id)
        if not message_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

        return crud.user_message.update(db=db, db_obj=message_model, obj_in=message_update_input)


user_message_service = UserMessageService()


