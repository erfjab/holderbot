from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.settings.utils.helpers import is_valid_input
from app.keys import BotKeys, PageCB, Pages, Actions, SelectCB
from app.models.server import ServerTypes
from app.db import crud
from app.api import ClinetManager

router = Router()


class ServerCreateForm(StatesGroup):
    REMARK = State()
    TYPES = State()
    DATA = State()


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.SERVERS)) & (F.action.is_(Actions.CREATE)))
)
async def create(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ServerCreateForm.REMARK)
    return await callback.message.edit_text(
        MessageTexts.ASK_REMARK, reply_markup=BotKeys.cancel()
    )


@router.message(StateFilter(ServerCreateForm.REMARK))
async def remark(message: Message, state: FSMContext):
    if not is_valid_input(message.text):
        track = await message.answer(MessageTexts.WRONG_STR)
        return await tracker.add(track)

    if await crud.get_server(message.text.lower()):
        track = await message.answer(MessageTexts.DUPLICATE)
        return await tracker.add(track)

    await state.set_state(ServerCreateForm.TYPES)
    await state.update_data(remark=message.text.lower())
    track = await message.answer(
        MessageTexts.ASK_TYPES,
        reply_markup=BotKeys.selector(
            [ServerTypes.MARZNESHIN, ServerTypes.MARZBAN],
            types=Pages.SERVERS,
            action=Actions.CREATE,
        ),
    )
    return await tracker.cleardelete(message, track)


@router.callback_query(
    StateFilter(ServerCreateForm.TYPES),
    SelectCB.filter((F.types.is_(Pages.SERVERS)) & (F.action.is_(Actions.CREATE))),
)
async def types(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    await state.update_data(types=callback_data.select)
    await state.set_state(ServerCreateForm.DATA)
    return await callback.message.edit_text(
        MessageTexts.ASK_MARZ_DATA, reply_markup=BotKeys.cancel()
    )


@router.message(StateFilter(ServerCreateForm.DATA))
async def data(message: Message, state: FSMContext):
    messages = message.text.split()
    if len(messages) != 3:
        track = await message.answer(MessageTexts.WRONG_PATTERN)
        return await tracker.add(track)

    state_data = await state.get_data()

    server_type_find = {
        ServerTypes.MARZNESHIN.value: ServerTypes.MARZNESHIN,
        ServerTypes.MARZBAN.value: ServerTypes.MARZBAN,
    }
    server_data = {
        "username": messages[0],
        "password": messages[1],
        "host": messages[2],
    }
    server_type = server_type_find.get(state_data["types"])
    token = await ClinetManager.generate_access(
        server_data,
        server_type,
    )
    if not token:
        track = await message.answer(MessageTexts.INVALID_DATA)
        return await tracker.add(track)

    server = await crud.create_server(
        remark=state_data["remark"],
        types=server_type,
        data=server_data,
    )
    await crud.upsert_server_access(serverid=server.id, serveraccess=token)
    text = MessageTexts.SUCCESS if server else MessageTexts.FAILED
    track = await message.answer(text, reply_markup=BotKeys.cancel())
    return await tracker.cleardelete(message, track)
