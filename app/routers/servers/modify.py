from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.db import crud
from app.models.server import MarzneshinServerData, ServerTypes
from app.keys import BotKeys, PageCB, Actions, Pages
from app.models.server import ServerModify
from app.settings.language import MessageTexts
from app.api import ClinetManager

router = Router(name="server_modify")


class ServerModifyForm(StatesGroup):
    ALL = State()


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.SERVERS)) & (F.action.is_(Actions.MODIFY)))
)
async def start_modify(
    callback: CallbackQuery, callback_data: PageCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        return await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )

    await state.clear()
    await state.set_state(ServerModifyForm.ALL)
    await state.update_data(serverid=server.id)
    await state.update_data(servertypes=server.types)
    await state.update_data(panel=callback_data.panel)
    match callback_data.datatype:
        case ServerModify.REMARK:
            await state.update_data(action=ServerModify.REMARK)
            text = MessageTexts.ASK_REMARK
        case ServerModify.DATA:
            await state.update_data(action=ServerModify.DATA)
            text = MessageTexts.ASK_MARZNESHIN_DATA
    return await callback.message.edit_text(text=text, reply_markup=BotKeys.cancel())


@router.message(StateFilter(ServerModifyForm.ALL))
async def finish_modify(message: Message, state: FSMContext):
    state_data = await state.get_data()
    serverid = int(state_data["serverid"])
    match state_data["action"]:
        case ServerModify.REMARK.value:
            if not message.text.isalpha():
                return await message.answer(MessageTexts.WRONG_STR)

            if await crud.get_server(message.text.lower()):
                return await message.answer(MessageTexts.DUPLICATE)

            server_modify = await crud.modify_server(serverid, remark=message.text)

        case ServerModify.DATA.value:
            messages = message.text.split()
            if len(messages) != 3:
                return await message.answer(MessageTexts.WRONG_PATTERN)

            server_type_find = {
                ServerTypes.MARZNESHIN.value: ServerTypes.MARZNESHIN,
            }
            server_data = MarzneshinServerData(
                username=messages[0], password=messages[1], host=messages[2]
            )
            server_type = server_type_find.get(state_data["servertypes"])
            token = await ClinetManager.generate_access(server_data.dict(), server_type)
            if not token:
                return await message.answer(MessageTexts.INVALID_DATA)

            server_modify = await crud.modify_server(
                serverid,
                data=server_data.dict(),
            )
    await state.clear()
    return await message.answer(
        text=MessageTexts.SUCCESS if server_modify else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(),
    )
