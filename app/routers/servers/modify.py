from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.db import crud
from app.models.server import ServerTypes
from app.keys import BotKeys, PageCB, Actions, Pages, YesOrNot, SelectCB
from app.models.server import ServerModify
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.track import tracker

router = Router(name="server_modify")


class ServerModifyForm(StatesGroup):
    ALL = State()
    REMOVE = State()


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.SERVERS)) & (F.action.is_(Actions.MODIFY)))
)
async def start_modify(
    callback: CallbackQuery, callback_data: PageCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.clear()
    await state.update_data(serverid=server.id)
    await state.update_data(servertypes=server.types)
    await state.update_data(panel=callback_data.panel)
    match callback_data.datatype:
        case ServerModify.REMARK:
            await state.update_data(action=ServerModify.REMARK)
            text = MessageTexts.ASK_REMARK
        case ServerModify.DATA:
            await state.update_data(action=ServerModify.DATA)
            text = MessageTexts.ASK_MARZ_DATA
        case ServerModify.REMOVE:
            await state.set_state(ServerModifyForm.REMOVE)
            return await callback.message.edit_text(
                text=MessageTexts.ASK_SURE,
                reply_markup=BotKeys.selector(
                    data=[YesOrNot.YES, YesOrNot.NO],
                    types=Pages.SERVERS,
                    action=Actions.MODIFY,
                    panel=server.id,
                ),
            )

    await state.set_state(ServerModifyForm.ALL)
    return await callback.message.edit_text(text=text, reply_markup=BotKeys.cancel())


@router.message(StateFilter(ServerModifyForm.ALL))
async def finish_modify(message: Message, state: FSMContext):
    state_data = await state.get_data()
    serverid = int(state_data["serverid"])
    match state_data["action"]:
        case ServerModify.REMARK.value:
            if not message.text.isalpha():
                track = await message.answer(MessageTexts.WRONG_STR)
                return await tracker.add(track)

            if await crud.get_server(message.text.lower()):
                track = await message.answer(MessageTexts.DUPLICATE)
                return await tracker.add(track)

            server_modify = await crud.modify_server(serverid, remark=message.text)

        case ServerModify.DATA.value:
            messages = message.text.split()
            if len(messages) != 3:
                track = await message.answer(MessageTexts.WRONG_PATTERN)
                return await tracker.add(track)

            server_type_find = {
                ServerTypes.MARZNESHIN.value: ServerTypes.MARZNESHIN,
            }
            server_data = {
                "username": messages[0],
                "password": messages[1],
                "host": messages[2],
            }
            server_type = server_type_find.get(state_data["servertypes"])
            token = await ClinetManager.generate_access(server_data, server_type)
            if not token:
                track = await message.answer(MessageTexts.INVALID_DATA)
                return await tracker.add(track)

            server_modify = await crud.modify_server(
                serverid,
                data=server_data,
            )
    await state.clear()
    track = await message.answer(
        text=MessageTexts.SUCCESS if server_modify else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(),
    )
    return await tracker.cleardelete(message, track)


@router.callback_query(
    StateFilter(ServerModifyForm.REMOVE),
    SelectCB.filter((F.types.is_(Pages.SERVERS)) & (F.action.is_(Actions.MODIFY))),
)
async def remove(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    if callback_data.select == YesOrNot.NO.value:
        track = await callback.message.edit_text(
            text=MessageTexts.FAILED, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await crud.remove_server(serverid=server.id)
    return await callback.message.edit_text(
        text=MessageTexts.SUCCESS,
        reply_markup=BotKeys.cancel(),
    )
