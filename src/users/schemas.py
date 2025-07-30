from pydantic import BaseModel
from datetime import datetime

class GetAllUsers(BaseModel):
    id: str
    username: str
    email: str
    first_name: str | None
    last_name: str | None
    is_active: bool | None
    created_at: datetime
    modified_at: datetime


class UserCreate(BaseModel):
    username: str
    email: str

class UserChange(BaseModel):
    username: str
    email: str
    first_name: str | None
    last_name: str | None
    is_active: bool | None
    modified_at: datetime