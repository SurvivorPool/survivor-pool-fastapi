from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str):
        return db.query(User).filter(email=email).first()


user = CRUDUser(User)

