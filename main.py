import os, sys
import uvicorn
from fastapi_sqlalchemy import DBSessionMiddleware, db
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from dotenv import load_dotenv
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
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Hello World!"}
