from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import dependencies
from schemas.stats import LeagueStats, PreviousWeekPick, StatsResponse
from services.league import league_service
from services.pick import pick_service

authorized_router = APIRouter(
    prefix="/stats",
    tags=['stats'],
    dependencies=[Depends(dependencies.get_current_user)]
)


@authorized_router.get('/{league_id}')
def get_stats(league_id: UUID, db: Session = Depends(dependencies.get_db)):
    league_picks = pick_service.get_previous_week_picks_for_league(db, league_id)
    all_picks = pick_service.get_all_picks(db)
    league_model = league_service.get_by_id(db, league_id)

    teams = league_model.teams
    active_count = 0
    inactive_count = 0

    for team in league_model.teams:
        if team.active:
            active_count += 1
        else:
            inactive_count += 1

    previous_week_picks_current_league_response = [PreviousWeekPick(team_name=pick.nfl_team_name, count=pick.count)
                                                   for pick in league_picks]
    previous_week_picks_all_leagues_response = [PreviousWeekPick(team_name=pick.nfl_team_name, count=pick.count)
                                                for pick in all_picks]

    league_stats = LeagueStats(
        active=active_count,
        inactive=inactive_count,
        total=len(teams)
    )

    stats_response = StatsResponse(previous_week_picks_current_league=previous_week_picks_current_league_response, previous_week_picks_all_leagues=previous_week_picks_all_leagues_response, league_stats=league_stats)
    return stats_response




