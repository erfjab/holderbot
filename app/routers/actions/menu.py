from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.models.action import ActionTypes
from app.models.server import ServerTypes

router = Router(name="actions_menu")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.ACTIONS)) & (F.action.is_(Actions.LIST)))
)
async def data(callback: CallbackQuery, callback_data: PageCB):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)
    menu_keys = [
        ActionTypes.ACTIVATED_USERS,
        ActionTypes.DISABLED_USERS,
        ActionTypes.DELETE_EXPIRED_USERS,
        ActionTypes.DELETE_LIMITED_USERS,
        ActionTypes.DELETE_USERS,
        ActionTypes.TRANSFER_USERS,
    ]
    if server.types == ServerTypes.MARZNESHIN.value:
        menu_keys.append(ActionTypes.ADD_CONFIG)
        menu_keys.append(ActionTypes.DELETE_CONFIG)
    return await callback.message.edit_text(
        text=MessageTexts.ITEMS,
        reply_markup=BotKeys.selector(
            data=menu_keys,
            types=Pages.ACTIONS,
            action=Actions.INFO,
            panel=server.id,
            server_back=server.id,
        ),
    )
