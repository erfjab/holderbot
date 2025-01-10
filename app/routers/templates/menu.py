from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts

router = Router(name="templates_menu")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.TEMPLATES)) & (F.action.is_(Actions.LIST)))
)
async def menu(callback: CallbackQuery):
    templates = await crud.get_templates()
    return await callback.message.edit_text(
        text=MessageTexts.ITEMS,
        reply_markup=BotKeys.lister(
            items=[tem for tem in templates], page=Pages.TEMPLATES
        ),
    )
