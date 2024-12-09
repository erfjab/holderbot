from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart

from app.settings import MessageText
from app.keys import Keyboards, PageCB, Pages

from app.db import crud

router = Router()


@router.message(CommandStart(ignore_case=True))
async def start(message: Message):
    """home page handler"""
    servers = await crud.get_servers()
    return await message.answer(
        text=MessageText.HOME, reply_markup=Keyboards.home(servers)
    )


@router.callback_query(PageCB.filter(F.page.is_(Pages.HOME)))
async def home(callback: CallbackQuery):
    """back or update home page handler"""
    servers = await crud.get_servers()
    return await callback.message.edit_text(
        text=MessageText.HOME, reply_markup=Keyboards.home(servers)
    )
