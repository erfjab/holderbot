from sqlalchemy.future import select
from db.base import GetDB
from db.models import Token
from models import (
    TokenUpsert,
    TokenData,
)


class TokenManager:

    @staticmethod
    async def upsert(token_upsert: TokenUpsert) -> TokenData:
        async with GetDB() as db:
            existing_token = await db.execute(select(Token).where(Token.id == 1))
            token = existing_token.scalar_one_or_none()

            if token:
                token.token = token_upsert.token
            else:
                token = Token(id=1, token=token_upsert.token)

            db.add(token)
            await db.commit()
            await db.refresh(token)
            return TokenData.from_orm(token)

    @staticmethod
    async def get() -> TokenData:
        async with GetDB() as db:
            result = await db.execute(select(Token).where(Token.id == 1))
            token = result.scalar_one_or_none()
            return TokenData.from_orm(token) if token else None
