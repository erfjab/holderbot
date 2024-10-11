from pydantic import BaseModel
from datetime import datetime


class TokenData(BaseModel):
    id: int
    token: str
    updated_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class TokenUpsert(BaseModel):
    token: str
