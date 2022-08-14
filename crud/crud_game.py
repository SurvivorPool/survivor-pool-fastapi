from crud.base import CRUDBase
from models.game import Game
from schemas.game import GameCreate, GameUpdate


class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate]):
    ...


game = CRUDGame(Game)