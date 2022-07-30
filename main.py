import os
import uvicorn
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
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ["PORT"])