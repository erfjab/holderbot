from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from utils.statedb import storage
from utils.lang import MessageTexts
from utils.keys import BotKeyboards
from models import PagesCallbacks, PagesActions

router = Router()


@router.message(CommandStart(ignore_case=True))
async def start(message: Message, state: FSMContext):
    await state.clear()
    new_message = await message.answer(
        text=MessageTexts.Start, reply_markup=BotKeyboards.home()
    )
    return await storage.clear_and_add_message(new_message)


@router.callback_query(PagesCallbacks.filter(F.page.is_(PagesActions.Home)))
async def home(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    new_message = await callback.message.answer(
        text=MessageTexts.Start, reply_markup=BotKeyboards.home()
    )
    return await storage.clear_and_add_message(new_message)


@router.message(Command(commands=["version", "v"]))
async def version(message: Message):
    new_message = await message.answer(text=MessageTexts.Version)
    return await storage.clear_and_add_message(new_message)
