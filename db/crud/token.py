"""
This module provides functionality for managing tokens in the application.

It includes methods for upserting and retrieving tokens from the database.
"""

from sqlalchemy.future import select
from db.base import get_db
from db.models import Token
from models import TokenUpsert, TokenData


class TokenManager:
    """Manager class for handling token operations."""

    @staticmethod
    async def upsert(token_upsert: TokenUpsert) -> TokenData:
        """
        Upsert a token in the database.

        If the token with ID 1 exists, it will be updated. If it does not exist,
        a new token will be created with ID 1.

        Args:
            token_upsert (TokenUpsert): The token data to upsert.

        Returns:
            TokenData: The upserted token data.
        """
        async with get_db() as db:
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
        """
        Retrieve the token with ID 1 from the database.

        Returns:
            TokenData | None: The retrieved token data or None if not found.
        """
        async with get_db() as db:
            result = await db.execute(select(Token).where(Token.id == 1))
            token = result.scalar_one_or_none()
            return TokenData.from_orm(token) if token else None
