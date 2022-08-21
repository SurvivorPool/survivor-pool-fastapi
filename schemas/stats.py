from pydantic import BaseModel


class PreviousWeekPick(BaseModel):
    team_name: str
    count: int


class LeagueStats(BaseModel):
    active: int
    inactive: int
    total: int


class StatsResponse(BaseModel):
    previous_week_picks_current_league: list[PreviousWeekPick]
    previous_week_picks_all_leagues: list[PreviousWeekPick]
    league_stats: LeagueStats
