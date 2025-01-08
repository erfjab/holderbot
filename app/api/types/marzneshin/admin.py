from pydantic import BaseModel


class MarzneshinToken(BaseModel):
    access_token: str
    is_sudo: bool
    token_type: str = "bearer"


class MarzneshinAdmin(BaseModel):
    username: str
    is_sudo: bool
    enabled: bool = True
    all_services_access: bool = False
    modify_users_access: bool = True
    service_ids: list = []
    subscription_url_prefix: str = ""
    users_data_usage: int
