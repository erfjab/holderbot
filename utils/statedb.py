# pylint: disable=all
# because this is a plugin

from typing import Any, Dict, Optional, List, Union
from sqlalchemy import Column, Integer, String, JSON, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery
import asyncio
from contextlib import asynccontextmanager

Base = declarative_base()

# Constants
DATABASE_URL = "sqlite+aiosqlite:///data/state.db"


# Model Classes
class StateModel(Base):
    __tablename__ = "states"
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)
    state = Column(String)


class DataModel(Base):
    __tablename__ = "data"
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)
    data = Column(JSON)


class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, index=True)
    message_id = Column(Integer, index=True)


class SQLAlchemyStorage(BaseStorage):
    def __init__(self, db_url: str = DATABASE_URL):
        self.engine = create_async_engine(db_url, echo=False)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self._connection_lock = asyncio.Lock()

    @asynccontextmanager
    async def session(self):
        await self.init()
        async with self._connection_lock:
            async with self.async_session() as session:
                async with session.begin():
                    yield session

    async def init(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def set_state(self, key: StorageKey, state: Optional[State] = None) -> None:
        async with self.session() as session:
            if state is None:
                await session.execute(
                    StateModel.__table__.delete().where(
                        and_(
                            StateModel.user_id == key.user_id,
                            StateModel.chat_id == key.chat_id,
                        )
                    )
                )
            else:
                state_str = state.state if isinstance(state, State) else state
                await session.merge(
                    StateModel(
                        user_id=key.user_id, chat_id=key.chat_id, state=state_str
                    )
                )

    async def get_state(self, key: StorageKey) -> Optional[str]:
        async with self.session() as session:
            result = await session.execute(
                select(StateModel).where(
                    and_(
                        StateModel.user_id == key.user_id,
                        StateModel.chat_id == key.chat_id,
                    )
                )
            )
            state = result.scalar_one_or_none()
            return state.state if state else None

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        async with self.session() as session:
            existing_data = await session.get(DataModel, (key.user_id, key.chat_id))
            if existing_data:
                existing_data.data = data
            else:
                new_data = DataModel(
                    user_id=key.user_id, chat_id=key.chat_id, data=data
                )
                session.add(new_data)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        async with self.session() as session:
            result = await session.get(DataModel, (key.user_id, key.chat_id))
            return result.data if result else {}

    async def add_log_message(self, chat_id: int, message_id: int) -> None:
        async with self.session() as session:
            new_log = MessageModel(chat_id=chat_id, message_id=message_id)
            session.add(new_log)

    async def delete_log_messages(self, chat_id: int) -> int:
        async with self.session() as session:
            result = await session.execute(
                MessageModel.__table__.delete().where(MessageModel.chat_id == chat_id)
            )
            return result.rowcount

    async def get_log_messages(self, chat_id: int) -> List[int]:
        async with self.session() as session:
            result = await session.execute(
                select(MessageModel.message_id).where(MessageModel.chat_id == chat_id)
            )
            return [row[0] for row in result.fetchall()]

    async def clear_chat_messages(
        self, message_or_callback: Union[Message, CallbackQuery]
    ) -> None:
        chat_id = (
            message_or_callback.chat.id
            if isinstance(message_or_callback, Message)
            else message_or_callback.message.chat.id
        )

        message_ids = await self.get_log_messages(chat_id)

        for msg_id in message_ids:
            try:
                await message_or_callback.bot.delete_message(chat_id, msg_id)
            except Exception as e:
                print(f"Failed to delete message {msg_id}: {e}")

    async def clear_and_add_message(
        self, message_or_callback: Union[Message, CallbackQuery]
    ) -> None:
        chat_id = (
            message_or_callback.chat.id
            if isinstance(message_or_callback, Message)
            else message_or_callback.message.chat.id
        )

        message_ids = await self.get_log_messages(chat_id)

        for msg_id in message_ids:
            try:
                await message_or_callback.bot.delete_message(chat_id, msg_id)
            except Exception as e:
                print(f"Failed to delete message {msg_id}: {e}")

        await self.delete_log_messages(chat_id)

        message_id = (
            message_or_callback.message_id
            if isinstance(message_or_callback, Message)
            else message_or_callback.message.message_id
        )
        await self.add_log_message(chat_id, message_id)

    async def close(self) -> None:
        await self.engine.dispose()


storage = SQLAlchemyStorage()
