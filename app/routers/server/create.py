from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.settings import MessageText
from app.keys import Keyboards, PageCB, Pages, Actions, SelectCB
from app.models.server import ServerType, MarzServerData
from app.db import crud

router = Router()


class ServerCreateForm(StatesGroup):
    """new server create form"""

    REMARK = State()
    TYPE = State()
    DATA = State()


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.SERVER)) & (F.action.is_(Actions.CREATE)))
)
async def create(callback: CallbackQuery, state: FSMContext):
    """server create handler"""
    await state.set_state(ServerCreateForm.REMARK)
    return await callback.message.edit_text(
        MessageText.ASK_SERVER_REMARK, reply_markup=Keyboards.cancel()
    )


@router.message(StateFilter(ServerCreateForm.REMARK))
async def remark(message: Message, state: FSMContext):
    """server remark input handler"""
    if not message.text.isalpha():
        return await message.answer(MessageText.WRONG_STRING_INPUT)

    if await crud.get_server(message.text):
        return await message.answer(MessageText.DUPLICATE)

    await state.set_state(ServerCreateForm.TYPE)
    await state.update_data(remark=message.text)
    return await message.answer(
        MessageText.ASK_SERVER_TYPE,
        reply_markup=Keyboards.type_select(
            [ServerType.MARZBAN, ServerType.MARZNESHIN],
            types=Pages.SERVER,
            action=Actions.CREATE,
        ),
    )


@router.callback_query(
    StateFilter(ServerCreateForm.TYPE),
    SelectCB.filter((F.types.is_(Pages.SERVER)) & (F.action.is_(Actions.CREATE))),
)
async def types(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    """server type input handler"""
    await state.update_data(types=callback_data.data)
    await state.set_state(ServerCreateForm.DATA)
    return await callback.message.edit_text(
        MessageText.ASK_MARZ_SERVER_DATA, reply_markup=Keyboards.cancel()
    )


@router.message(StateFilter(ServerCreateForm.DATA))
async def data(message: Message, state: FSMContext):
    """server data input handler"""
    messages = message.text.split()
    if len(messages) > 3:
        return await message.answer(MessageText.SERVER_WRONG_DATA_INPUT)

    state_data = await state.get_data()

    server = await crud.create_server(
        remark=state_data["remark"],
        types=ServerType.MARZBAN
        if state_data["types"] == ServerType.MARZBAN.value
        else ServerType.MARZNESHIN,
        data=MarzServerData(
            username=messages[0], password=messages[1], host=messages[2]
        ).dict(),
    )
    text = MessageText.SUCCES if server else MessageText.FAILED
    servers = await crud.get_servers()
    return await message.answer(text, reply_markup=Keyboards.home(servers))
