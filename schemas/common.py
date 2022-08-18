from pydantic import BaseModel


class DeleteModel(BaseModel):
    success: bool
    detail: str
