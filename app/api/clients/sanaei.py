import json
from ..core import ApiRequest


class SanaeiApiManager(ApiRequest):
    async def get_token(self, username: str, password: str):
        data = {
            "username": username,
            "password": password,
        }
        res = await self.post(
            endpoint="/login",
            data=data,
            full=True,
        )
        return json.dumps(dict(res.cookies)) if res.cookies else None
