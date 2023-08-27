import os
from fastapi_sqlalchemy import DBSessionMiddleware
import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from starlette.middleware.sessions import SessionMiddleware
from core.config import settings
from api.v1.endpoints import admin_message, advance_week, game, \
    league, league_type, message_type, nfl_team, pick, player_team, stadium, stats, user


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World!"

schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
allow_all = ['*']
app.add_middleware(
   CORSMiddleware,
   allow_origins=[""],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

app.add_middleware(DBSessionMiddleware, db_url=settings.get_database_url())
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])
app.include_router(admin_message.admin_router)
app.include_router(admin_message.authorized_router)
app.include_router(advance_week.admin_router)
app.include_router(game.authorized_router)
app.include_router(league.admin_router)
app.include_router(league.authenticated_router)
app.include_router(league_type.admin_router)
app.include_router(message_type.admin_router)
app.include_router(nfl_team.authorized_router)
app.include_router(pick.authorized_router)
app.include_router(player_team.authorized_router)
app.include_router(player_team.admin_router)
app.include_router(stadium.authorized_router)
app.include_router(stats.authorized_router)
app.include_router(user.unauthorized_router)
app.include_router(user.authorized_router)
app.include_router(user.admin_router)


@app.get("/")
async def root():
    return {"message": "Hello World!!!!"}



