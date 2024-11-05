"""
Module defining token-related models.
"""

from datetime import datetime
from pydantic import BaseModel


class TokenData(BaseModel):
    """
    Model for representing a token with its associated data,
    including creation and update timestamps.
    """

    id: int
    token: str
    updated_at: datetime | None
    created_at: datetime

    # pylint: disable=R0903
    class Config:
        """Pydantic configuration options."""

        from_attributes = True


class TokenUpsert(BaseModel):
    """
    Model for upserting a token.
    """

    token: str
