from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud
from app.settings.utils.update import check_github_version
from app.version import __version__
from app.api import ClinetManager
from app.models.user import UserModify

router = Router(name="start")


@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    args = message.text.split()

    if len(args) >= 2 and args[1].startswith("user_"):
        try:
            await message.delete()
        except Exception:
            pass
        parts = args[1].split("_")

        if len(parts) >= 3:
            server_id = int(parts[1])
            username = "_".join(parts[2:])
            server = await crud.get_server(server_id)
            if not server:
                track = await message.answer(text=MessageTexts.NOT_FOUND)
                return await tracker.add(track)

            user = await ClinetManager.get_user(server, username)
            if not user:
                return await message.answer(text=MessageTexts.NOT_FOUND)

            track = await message.answer(
                text=user.format_data_str(),
                reply_markup=BotKeys.selector(
                    data=[
                        UserModify.DATA_LIMIT,
                        UserModify.DATE_LIMIT,
                        UserModify.DISABLED if user.is_active else UserModify.ACTIVATED,
                        UserModify.RESET_USAGE,
                        UserModify.REVOKE,
                        UserModify.QRCODE,
                        UserModify.NOTE,
                        UserModify.OWNER,
                        UserModify.CONFIGS,
                        UserModify.CHARGE,
                        UserModify.REMOVE,
                    ],
                    types=Pages.USERS,
                    action=Actions.MODIFY,
                    extra=user.username,
                    panel=server.id,
                    server_back=server.id,
                ),
            )
            return await tracker.add(track)

    await state.clear()
    servers = await crud.get_servers()
    track = await message.answer(
        text=MessageTexts.START, reply_markup=BotKeys.home(servers)
    )
    return await tracker.cleardelete(message, track)


@router.callback_query(PageCB.filter(F.page.is_(Pages.HOME)))
async def home(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    servers = await crud.get_servers()
    track = await callback.message.answer(
        text=MessageTexts.START, reply_markup=BotKeys.home(servers)
    )
    return await tracker.cleardelete(callback, track)


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.MENU)) & (F.action.is_(Actions.LIST)))
)
async def menu(callback: CallbackQuery, callback_data: PageCB, state: FSMContext):
    await state.clear()
    return await callback.message.edit_text(
        text=MessageTexts.MENU, reply_markup=BotKeys.menu(panel=callback_data.panel)
    )


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.UPDATE)) & (F.action.is_(Actions.INFO)))
)
async def updatechecker(
    callback: CallbackQuery, callback_data: PageCB, state: FSMContext
):
    await state.clear()
    has_update, latest_version = await check_github_version(__version__)
    return await callback.answer(
        text="You are update!" if not has_update else "🎉 New version is ready!",
        show_alert=True,
    )
