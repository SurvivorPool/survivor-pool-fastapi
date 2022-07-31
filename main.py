import os
from fastapi_sqlalchemy import DBSessionMiddleware, db
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from dotenv import load_dotenv

from routers import auth


load_dotenv(".env")


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World!"


schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World!!!!"}



