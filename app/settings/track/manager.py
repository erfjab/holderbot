from typing import Any, Dict, Optional, List, Union
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery
from sqlalchemy.future import select
from sqlalchemy import and_

from .utils import DatabaseManager
from .models import StateModel, DataModel, MessageModel
from .config import engine


class SQLAlchemyStorage(BaseStorage):
    def __init__(self):
        self.db = DatabaseManager()

    async def set_state(self, key: StorageKey, state: Optional[State] = None) -> None:
        async with self.db.session() as session:
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
        async with self.db.session() as session:
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
        async with self.db.session() as session:
            existing_data = await session.get(DataModel, (key.user_id, key.chat_id))
            if existing_data:
                existing_data.data = data
            else:
                new_data = DataModel(
                    user_id=key.user_id, chat_id=key.chat_id, data=data
                )
                session.add(new_data)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        async with self.db.session() as session:
            result = await session.get(DataModel, (key.user_id, key.chat_id))
            return result.data if result else {}

    # tarcker handlers
    async def add(self, update: Message | CallbackQuery) -> None:
        async with self.db.session() as session:
            message = update.message if isinstance(update, CallbackQuery) else update
            new_log = MessageModel(
                chat_id=update.chat.id, message_id=message.message_id
            )
            session.add(new_log)

    async def delete(self, chat_id: int) -> int:
        async with self.db.session() as session:
            result = await session.execute(
                MessageModel.__table__.delete().where(MessageModel.chat_id == chat_id)
            )
            return result.rowcount

    async def get(self, chat_id: int) -> List[int]:
        async with self.db.session() as session:
            result = await session.execute(
                select(MessageModel.message_id).where(MessageModel.chat_id == chat_id)
            )
            return [row[0] for row in result.fetchall()]

    async def clear(self, update: Union[Message, CallbackQuery]) -> None:
        chatid = (
            update.message.chat.id
            if isinstance(update, CallbackQuery)
            else update.chat.id
        )
        message_ids = await self.get(chatid)

        try:
            await update.bot.delete_messages(chatid, message_ids)
        except Exception:
            pass

        await self.delete(chatid)

    async def cleardelete(
        self,
        user: Union[Message, CallbackQuery],
        update: Union[Message, CallbackQuery] = None,
    ) -> None:
        await self.clear(user)
        await self.add(update)

    async def close(self) -> None:
        await engine.dispose()
