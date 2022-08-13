from crud.base import CRUDBase
from models.stadium import Stadium
from schemas.stadium import StadiumCreate, StadiumUpdate


class CRUDStadium(CRUDBase[Stadium, StadiumCreate, StadiumUpdate]):
    ...


stadium = CRUDStadium(Stadium)
