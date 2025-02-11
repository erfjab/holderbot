from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.settings.utils.helpers import is_valid_input
from app.keys import BotKeys, PageCB, Pages, Actions, SelectCB
from app.models.user import DateTypes
from app.db import crud

router = Router()


class TemplateCreateForm(StatesGroup):
    REMARK = State()
    TYPES = State()
    DATA_LIMIT = State()
    DATE_LIMIT = State()
    DATE_TYPES = State()


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.TEMPLATES)) & (F.action.is_(Actions.CREATE)))
)
async def create(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TemplateCreateForm.REMARK)
    return await callback.message.edit_text(
        MessageTexts.ASK_REMARK, reply_markup=BotKeys.cancel()
    )


@router.message(StateFilter(TemplateCreateForm.REMARK))
async def remark(message: Message, state: FSMContext):
    if not is_valid_input(text=message.text):
        track = await message.answer(MessageTexts.WRONG_STR)
        return await tracker.add(track)

    if await crud.get_template(message.text.lower()):
        track = await message.answer(MessageTexts.DUPLICATE)
        return await tracker.add(track)

    await state.update_data(remark=message.text.lower())
    await state.set_state(TemplateCreateForm.DATA_LIMIT)
    track = await message.answer(
        MessageTexts.ASK_DATA_LIMT, reply_markup=BotKeys.cancel()
    )
    return await tracker.cleardelete(message, track)


@router.message(StateFilter(TemplateCreateForm.DATA_LIMIT))
async def data(message: Message, state: FSMContext):
    if not message.text.isdigit():
        track = await message.answer(text=MessageTexts.WRONG_INT)
        return await tracker.add(track)

    await state.update_data(datalimit=message.text)
    await state.set_state(TemplateCreateForm.DATE_TYPES)
    track = await message.answer(
        text=MessageTexts.MENU,
        reply_markup=BotKeys.selector(
            data=[DateTypes.UNLIMITED, DateTypes.NOW, DateTypes.AFTER_FIRST_USE],
            types=Pages.TEMPLATES,
            action=Actions.CREATE,
            width=1,
        ),
    )
    return await tracker.cleardelete(message, track)


@router.callback_query(
    StateFilter(TemplateCreateForm.DATE_TYPES),
    SelectCB.filter((F.types.is_(Pages.TEMPLATES)) & (F.action.is_(Actions.CREATE))),
)
async def datetypes(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    await state.set_state(TemplateCreateForm.DATE_LIMIT)
    if callback_data.select == DateTypes.UNLIMITED.value:
        data = await state.get_data()
        template = await crud.create_template(
            remark=data["remark"],
            data_limit=int(data["datalimit"]),
            date_limit=0,
            date_types=callback_data.select,
        )
        return await callback.message.edit_text(
            text=MessageTexts.SUCCESS if template else MessageTexts.FAILED,
            reply_markup=BotKeys.cancel(),
        )

    await state.update_data(datatypes=callback_data.select)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_DATE_LIMIT, reply_markup=BotKeys.cancel()
    )


@router.message(StateFilter(TemplateCreateForm.DATE_LIMIT))
async def datelimit(message: Message, state: FSMContext):
    if not message.text.isdigit():
        track = await message.answer(text=MessageTexts.WRONG_INT)
        return await tracker.add(track)

    data = await state.get_data()
    template = await crud.create_template(
        remark=data["remark"],
        data_limit=int(data["datalimit"]),
        date_limit=int(message.text),
        date_types=data["datatypes"],
    )
    track = await message.answer(
        text=MessageTexts.SUCCESS if template else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(),
    )
    await tracker.cleardelete(message, track)
