"""
This module defines the base router for handling commands and callbacks in the bot.
It includes handlers for commands like start and version, and processes specific callback queries.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from utils import MessageTexts, Storage, BotKeyboards
from models import PagesCallbacks, PagesActions

router = Router()


@router.message(CommandStart(ignore_case=True))
async def start(message: Message, state: FSMContext):
    """
    Handler for the '/start' command. It clears the user's state and sends the start message
    with the home keyboard.
    """
    await state.clear()
    new_message = await message.answer(
        text=MessageTexts.START, reply_markup=BotKeyboards.home()
    )
    return await Storage.clear_and_add_message(new_message)


@router.callback_query(PagesCallbacks.filter(F.page.is_(PagesActions.HOME)))
async def home(callback: CallbackQuery, state: FSMContext):
    """
    Callback handler for the 'HOME' page action. Clears the state and sends the start message
    with the home keyboard again.
    """
    await state.clear()
    new_message = await callback.message.answer(
        text=MessageTexts.START, reply_markup=BotKeyboards.home()
    )
    return await Storage.clear_and_add_message(new_message)


@router.message(Command(commands=["version", "v"]))
async def version(message: Message):
    """
    Handler for the '/version' and '/v' commands. Sends the version information of the bot.
    """
    new_message = await message.answer(text=MessageTexts.VERSION)
    return await Storage.clear_and_add_message(new_message)
