from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud

router = Router(name="start")


@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
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
