from pydantic import BaseModel
from typing import Optional


class Training(BaseModel):
    name: str


class Task(BaseModel):
    name: str
    load: Optional[int]
    number: int


class TaskId(BaseModel):
    id: int
