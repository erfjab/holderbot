from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keys import BotKeys, Pages, PageCB, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.track import tracker


class UserSearchForm(StatesGroup):
    USERNAME = State()


router = Router(name="users_search")


@router.message(Command(commands=["user"]))
async def data(message: Message):
    try:
        _, serverid, username = message.text.split(maxsplit=2)
    except ValueError:
        track = await message.reply(
            text=f"{MessageTexts.WRONG_PATTERN}\n/user serverid username",
        )
        return await tracker.add(track)

    server = await crud.get_server(int(serverid))
    if not server:
        track = await message.reply(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    users = await ClinetManager.get_users(server, page=1, size=10, search=username)

    track = await message.answer(
        text=MessageTexts.ITEMS,
        reply_markup=BotKeys.lister(
            items=users,
            page=Pages.USERS,
            panel=server.id,
            search=True,
            server_back=server.id,
        ),
    )
    return await tracker.cleardelete(message, track)


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.USERS)) & (F.action.is_(Actions.SEARCH)))
)
async def start_search(
    callback: CallbackQuery, callback_data: PageCB, state: FSMContext
):
    server = await crud.get_server(int(callback_data.panel))
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)
    await state.set_state(UserSearchForm.USERNAME)
    await state.update_data(serverid=server.id)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_USERNAME,
        reply_markup=BotKeys.cancel(server_back=server.id),
    )


@router.message(StateFilter(UserSearchForm.USERNAME))
async def end_search(message: Message, state: FSMContext):
    server = await crud.get_server(int(await state.get_value("serverid")))
    if not server:
        track = await message.answer(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    users = await ClinetManager.get_users(server, page=1, size=10, search=message.text)

    track = await message.answer(
        text=MessageTexts.ITEMS,
        reply_markup=BotKeys.lister(
            items=users,
            page=Pages.USERS,
            panel=server.id,
            search=True,
            server_back=server.id,
        ),
    )
    return await tracker.cleardelete(message, track)
