from uuid import UUID
from sqlalchemy.orm import Session
import crud
from models import User
from schemas.user import UserUpdate, UserCreate


class UserService:
    def get_by_id(self, db: Session, user_id: UUID):
        return crud.user.get(db, user_id)

    def get_all(self, db: Session):
        return crud.user.get_multi(db=db)

    def get_by_email_and_provider(
            self,
            db: Session,
            email: str,
            provider: str
    ):
        user_model = crud.user.get_by_email_and_provider(db=db, email=email, provider=provider)
        return user_model

    def create(self, db: Session, user_create: UserCreate):
        return crud.user.create(db, obj_in=user_create)

    def update_user(
            self,
            db: Session,
            existing_model: User,
            user_update_input: UserUpdate
    ):
        user_model = crud.user.update(db, db_obj=existing_model, obj_in=user_update_input)
        return user_model







user_service = UserService()