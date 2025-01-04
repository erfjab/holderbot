from pydantic import BaseModel


class MarzneshinServiceResponce(BaseModel):
    id: int
    name: str | None
    inbound_ids: list[int]
    user_ids: list[int]
