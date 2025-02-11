from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.db import crud
from app.keys import BotKeys, Actions, Pages, SelectCB
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.settings.utils.helpers import is_valid_input
from .base import TemplateModifyForm
from app.models.template import TemplateModify

router = Router(name="template_modify_remark")


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.TEMPLATES))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [TemplateModify.REMARK.value],
            )
        )
    )
)
async def start_modify(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    await state.clear()
    await state.update_data(templateid=callback_data.extra)
    await state.set_state(TemplateModifyForm.INPUT)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_REMARK, reply_markup=BotKeys.cancel()
    )


@router.message(StateFilter(TemplateModifyForm.INPUT))
async def finish_modify(message: Message, state: FSMContext):
    state_data = await state.get_data()
    templateid = state_data["templateid"]
    if not is_valid_input(text=message.text):
        track = await message.answer(MessageTexts.WRONG_STR)
        return await tracker.add(track)

    if await crud.get_template(message.text.lower()):
        track = await message.answer(MessageTexts.DUPLICATE)
        return await tracker.add(track)

    template = await crud.modify_template(templateid, remark=message.text.lower())

    await state.clear()
    track = await message.answer(
        text=MessageTexts.SUCCESS if template else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(),
    )
    return await tracker.cleardelete(message, track)
