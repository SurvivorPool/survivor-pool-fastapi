from uuid import UUID
from sqlalchemy.orm import Session
import crud
from models import User
from schemas.user import UserUpdate, UserCreate, UserUpdateAdmin


class UserService:
    def get_by_id(self, db: Session, user_id: str):
        return crud.user.get(db, user_id)

    def get_all(self, db: Session):
        return crud.user.get_multi(db=db)

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

    def update_user_admin (
            self,
            db: Session,
            existing_model: User,
            user_update_input: UserUpdateAdmin
    ):
        user_model = crud.user.update(db, db_obj=existing_model, obj_in=user_update_input)
        return user_model







user_service = UserService()