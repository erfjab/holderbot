from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.models.template import TemplateModify

router = Router(name="template_data")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.TEMPLATES)) & (F.action.is_(Actions.INFO)))
)
async def data(callback: CallbackQuery, callback_data: PageCB):
    template = await crud.get_template(int(callback_data.dataid))
    if not template:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    return await callback.message.edit_text(
        text=template.format_data,
        reply_markup=BotKeys.selector(
            data=[
                TemplateModify.DATA_LIMIT,
                TemplateModify.DATE_LIMIT,
                TemplateModify.DISABLED
                if template.is_active
                else TemplateModify.ACTIVATED,
                TemplateModify.REMARK,
                TemplateModify.REMOVE,
            ],
            types=Pages.TEMPLATES,
            action=Actions.MODIFY,
            extra=callback_data.dataid,
        ),
    )
