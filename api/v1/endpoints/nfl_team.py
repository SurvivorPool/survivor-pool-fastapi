from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import dependencies
from services.nfl_team import nfl_team_service
from schemas.nfl_team import NFLTeamResponse, NFLTeamList

authorized_router = APIRouter(
    prefix="/nfl_teams",
    tags=["nfl teams"],
    dependencies=[Depends(dependencies.get_current_user)]
)


@authorized_router.get('', response_model=NFLTeamList)
async def nfl_teams(db: Session = Depends(dependencies.get_db)):
    await nfl_team_service.update_nfl_teams(db)
    nfl_team_models = nfl_team_service.get_teams(db)
    response_nfl_teams = []
    for nfl_team in nfl_team_models:
        response_nfl_team = NFLTeamResponse(**nfl_team.__dict__)
        response_nfl_teams.append(response_nfl_team)
    response = NFLTeamList(nfl_teams=response_nfl_teams)
    return response
