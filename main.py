import os
from fastapi_sqlalchemy import DBSessionMiddleware
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from starlette.middleware.sessions import SessionMiddleware
from core.config import settings
from api.v1.endpoints import admin_message, auth, game, league, league_type, message_type, nfl_team, pick, player_team, stadium, user



@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World!"


schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=settings.SQLALCHEMY_DATABASE_URI)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])
app.include_router(admin_message.admin_router)
app.include_router(admin_message.authorized_router)
app.include_router(auth.router)
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
app.include_router(user.unauthorized_router)
app.include_router(user.authorized_router)
app.include_router(user.admin_router)


@app.get("/")
async def root():
    return {"message": "Hello World!!!!"}



