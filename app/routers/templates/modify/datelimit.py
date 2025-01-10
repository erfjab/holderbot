from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.models.user import (
    DateTypes,
)
from app.models.template import TemplateModify
from .base import TemplateModifyForm


router = Router(name="template_modify_date_limit")


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.TEMPLATES))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [TemplateModify.DATE_LIMIT.value],
            )
        )
    )
)
async def selecttype(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    await state.set_state(TemplateModifyForm.DATE_TYPE)
    return await callback.message.edit_text(
        text=MessageTexts.MENU,
        reply_markup=BotKeys.selector(
            data=[DateTypes.UNLIMITED, DateTypes.NOW, DateTypes.AFTER_FIRST_USE],
            types=Pages.TEMPLATES,
            action=Actions.MODIFY,
            width=1,
            extra=callback_data.extra,
        ),
    )


@router.callback_query(
    StateFilter(TemplateModifyForm.DATE_TYPE),
    SelectCB.filter((F.types.is_(Pages.TEMPLATES)) & (F.action.is_(Actions.MODIFY))),
)
async def datelimit(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    if callback_data.select == DateTypes.UNLIMITED:
        template = await crud.modify_template(
            date_limit=0,
            date_types=callback_data.select,
        )
        return await callback.message.edit_text(
            text=MessageTexts.SUCCESS if template else MessageTexts.FAILED,
            reply_markup=BotKeys.cancel(),
        )

    await state.set_state(TemplateModifyForm.DATE_LIMIT)
    await state.update_data(templateid=callback_data.extra)
    await state.update_data(datatypes=callback_data.select)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_DATE_LIMIT, reply_markup=BotKeys.cancel()
    )


@router.message(StateFilter(TemplateModifyForm.DATE_LIMIT))
async def dateend(message: Message, state: FSMContext):
    if not message.text.isdigit() and int(message.text) <= 0:
        track = await message.answer(text=MessageTexts.WRONG_INT)
        return await tracker.add(track)

    data = await state.get_data()
    template = await crud.modify_template(
        date_limit=int(message.text),
        date_types=data["datatypes"],
    )
    track = await message.answer(
        text=MessageTexts.SUCCESS if template else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(),
    )
    await tracker.cleardelete(message, track)
