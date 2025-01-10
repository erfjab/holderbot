from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions, YesOrNot
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.models.template import TemplateModify
from .base import TemplateModifyForm

router = Router(name="template_modify_confirms")


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.TEMPLATES))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [
                    TemplateModify.ACTIVATED.value,
                    TemplateModify.DISABLED.value,
                    TemplateModify.REMOVE.value,
                ]
            )
        )
    )
)
async def confirmstart(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    await state.update_data(action=callback_data.select)
    await state.set_state(TemplateModifyForm.CONFIRM)

    return await callback.message.edit_text(
        text=MessageTexts.ASK_SURE,
        reply_markup=BotKeys.selector(
            data=[YesOrNot.YES, YesOrNot.NO],
            types=Pages.TEMPLATES,
            action=Actions.MODIFY,
            extra=callback_data.extra,
        ),
    )


@router.callback_query(
    StateFilter(TemplateModifyForm.CONFIRM),
    SelectCB.filter(
        (F.types.is_(Pages.TEMPLATES))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [
                    YesOrNot.YES,
                    YesOrNot.NO,
                ]
            )
        )
    ),
)
async def confirmend(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    if callback_data.select == YesOrNot.NO.value:
        track = await callback.message.edit_text(
            text=MessageTexts.FAILED, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    data = await state.get_data()

    match data["action"]:
        case TemplateModify.DISABLED:
            action = await crud.modify_template(
                templateid=callback_data.extra, is_active=False
            )

        case TemplateModify.ACTIVATED:
            action = await crud.modify_template(
                templateid=callback_data.extra, is_active=True
            )

        case TemplateModify.REMOVE:
            action = await crud.remove_template(templateid=callback_data.extra)

    return await callback.message.edit_text(
        text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(),
    )
