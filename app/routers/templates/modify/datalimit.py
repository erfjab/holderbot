from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from .base import TemplateModifyForm
from app.models.template import TemplateModify

router = Router(name="template_modify_data_limit")


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.TEMPLATES))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [TemplateModify.DATA_LIMIT.value],
            )
        )
    )
)
async def datestart(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    await state.update_data(action=callback_data.select)
    await state.update_data(template=callback_data.extra)
    await state.set_state(TemplateModifyForm.DATA_LIMIT)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_DATA_LIMT,
        reply_markup=BotKeys.cancel(),
    )


@router.message(StateFilter(TemplateModifyForm.DATA_LIMIT))
async def dateend(message: Message, state: FSMContext):
    if not message.text.isdigit():
        track = await message.answer(text=MessageTexts.WRONG_INT)
        return await tracker.add(track)

    data = await state.get_data()

    action = await crud.modify_template(
        templateid=data["template"], data_limit=int(message.text)
    )
    track = await message.answer(
        text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(),
    )
    return await tracker.cleardelete(message, track)
