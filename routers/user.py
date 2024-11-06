"""
This module contains the user-related callback functions and their handlers
for user creation and management.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from marzban import ProxyInbound

from utils import (
    panel,
    text_info,
    helpers,
    MessageTexts,
    storage,
    EnvSettings,
    BotKeyboards,
)
from models import (
    PagesActions,
    PagesCallbacks,
    AdminActions,
    UserCreateForm,
    UserStatusCallbacks,
    UserInboundsCallbacks,
    AdminSelectCallbacks,
)

router = Router()


@router.callback_query(PagesCallbacks.filter(F.page.is_(PagesActions.USER_CREATE)))
async def user_create(callback: CallbackQuery, state: FSMContext):
    """
    Initiates the user creation process by asking for the base username.
    """
    await state.set_state(UserCreateForm.base_username)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_CREATE_USER_BASE_USERNAME,
        reply_markup=BotKeyboards.cancel(),
    )


@router.message(StateFilter(UserCreateForm.base_username))
async def user_create_base_username(message: Message, state: FSMContext):
    """
    Handles the input for the base username in the user creation process.
    """
    await state.update_data(base_username=message.text)
    await state.set_state(UserCreateForm.start_number)
    new_message = await message.answer(
        text=MessageTexts.ASK_CREATE_USER_START_NUMBER,
        reply_markup=BotKeyboards.cancel(),
    )
    return await storage.clear_and_add_message(new_message)


@router.message(StateFilter(UserCreateForm.start_number))
async def user_create_start_number(message: Message, state: FSMContext):
    """
    Handles the input for the starting number in the user creation process.
    """
    if not message.text.isdigit():
        new_message = await message.answer(text=MessageTexts.JUST_NUMBER)
        return await storage.add_log_message(
            message.from_user.id, new_message.message_id
        )

    await state.update_data(start_number=int(message.text))
    await state.set_state(UserCreateForm.how_much)
    new_message = await message.answer(
        text=MessageTexts.ASK_CREATE_USER_HOW_MUCH, reply_markup=BotKeyboards.cancel()
    )
    return await storage.clear_and_add_message(new_message)


@router.message(StateFilter(UserCreateForm.how_much))
async def user_create_how_much(message: Message, state: FSMContext):
    """
    Handles the input for the 'how much' field in the user creation process.
    """
    if not message.text.isdigit():
        new_message = await message.answer(text=MessageTexts.JUST_NUMBER)
        return await storage.add_log_message(
            message.from_user.id, new_message.message_id
        )

    await state.update_data(how_much=int(message.text))
    await state.set_state(UserCreateForm.data_limit)
    new_message = await message.answer(
        text=MessageTexts.ASK_CREATE_USER_DATA_LIMIT, reply_markup=BotKeyboards.cancel()
    )
    return await storage.clear_and_add_message(new_message)


@router.message(StateFilter(UserCreateForm.data_limit))
async def user_create_data_limit(message: Message, state: FSMContext):
    """
    Handles the input for the data limit in the user creation process.
    """
    if not message.text.isdigit():
        new_message = await message.answer(text=MessageTexts.JUST_NUMBER)
        return await storage.add_log_message(
            message.from_user.id, new_message.message_id
        )

    await state.update_data(data_limit=int(message.text))
    await state.set_state(UserCreateForm.date_limit)
    new_message = await message.answer(
        text=MessageTexts.ASK_CREATE_USER_DATE_LIMIT, reply_markup=BotKeyboards.cancel()
    )
    return await storage.clear_and_add_message(new_message)


@router.message(StateFilter(UserCreateForm.date_limit))
async def user_create_date_limit(message: Message, state: FSMContext):
    """
    Handles the input for the date limit in the user creation process.
    """
    if not message.text.isdigit():
        new_message = await message.answer(text=MessageTexts.JUST_NUMBER)
        return await storage.add_log_message(
            message.from_user.id, new_message.message_id
        )

    await state.update_data(date_limit=int(message.text))
    new_message = await message.answer(
        text=MessageTexts.ASK_CREATE_USER_STATUS,
        reply_markup=BotKeyboards.user_status(AdminActions.ADD),
    )
    return await storage.clear_and_add_message(new_message)


@router.callback_query(UserStatusCallbacks.filter(F.action.is_(AdminActions.ADD)))
async def user_create_status(
    callback: CallbackQuery, callback_data: UserStatusCallbacks, state: FSMContext
):
    """
    Handles the status selection for user creation.
    """
    await state.update_data(status=callback_data.status)
    admins = await panel.admins()
    return await callback.message.edit_text(
        text=MessageTexts.ASK_CREATE_ADMIN_USERNAME,
        reply_markup=BotKeyboards.admins(admins),
    )


@router.callback_query(AdminSelectCallbacks.filter())
async def user_create_owner_select(
    callback: CallbackQuery, callback_data: AdminSelectCallbacks, state: FSMContext
):
    """
    Handles the selection of the admin owner during the user creation process.
    """
    await state.update_data(admin=callback_data.username)
    inbounds = await panel.get_inbounds()
    tags = [item['tag'] for sublist in inbounds.values() for item in sublist]
    await state.update_data(inbounds=inbounds)
    await state.update_data(selected_inbounds=tags)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_CREATE_USER_INBOUNDS,
        reply_markup=BotKeyboards.inbounds(inbounds, tags),
    )


@router.callback_query(
    UserInboundsCallbacks.filter(
        (
            F.action.is_(AdminActions.ADD)
            & (F.is_done.is_(False))
            & (F.just_one_inbound.is_(False))
        )
    )
)
async def user_create_inbounds(
    callback: CallbackQuery,
    callback_data: UserInboundsCallbacks,
    state: FSMContext,
):
    """
    Handles the inbound selection for user creation.
    """
    data = await state.get_data()
    inbounds = data.get("inbounds")
    selected_inbounds = set(data.get("selected_inbounds", []))

    if callback_data.is_selected is False:
        selected_inbounds.add(callback_data.tag)
    else:
        selected_inbounds.discard(callback_data.tag)

    await state.update_data(selected_inbounds=list(selected_inbounds))
    await callback.message.edit_reply_markup(
        reply_markup=BotKeyboards.inbounds(inbounds, selected_inbounds)
    )


@router.callback_query(
    UserInboundsCallbacks.filter(
        (
            F.action.is_(AdminActions.ADD)
            & (F.is_done.is_(True))
            & (F.just_one_inbound.is_(False))
        )
    )
)
async def user_create_inbounds_save(callback: CallbackQuery, state: FSMContext):
    """
    Saves the selected inbounds and creates users with the provided information.
    """
    data = await state.get_data()
    inbounds: dict[str, list[ProxyInbound]] = data.get("inbounds")
    selected_inbounds = set(data.get("selected_inbounds", []))

    if not selected_inbounds:
        return await callback.answer(
            text=MessageTexts.NONE_USER_INBOUNDS, show_alert=True
        )

    proxies = {
        inbound["protocol"]: {}
        for protocol_list in inbounds.values()
        for inbound in protocol_list
        if inbound["tag"] in selected_inbounds
    }

    inbounds_dict = {
        protocol: [
            inbound["tag"]
            for inbound in protocol_list
            if inbound["protocol"] == protocol and inbound["tag"] in selected_inbounds
        ]
        for protocol, protocol_list in inbounds.items()
    }
    inbounds_dict = {k: v for k, v in inbounds_dict.items() if v}

    for i in range(int(data["how_much"])):
        username = f"{data['base_username']}{int(data['start_number']) + i}"
        new_user = await panel.create_user(
            username=username,
            status=data["status"],
            proxies=proxies,
            inbounds=inbounds_dict,
            data_limit=data["data_limit"],
            date_limit=data["date_limit"],
        )

        if new_user:
            if data["admin"] != EnvSettings.MARZBAN_USERNAME:
                await panel.set_owner(data["admin"], new_user.username)
            qr_bytes = await helpers.create_qr(new_user.subscription_url)
            await callback.message.answer_photo(
                caption=text_info.user_info(new_user),
                photo=BufferedInputFile(qr_bytes, filename="qr_code.png"),
                reply_markup=BotKeyboards.user(new_user),
            )
        else:
            await callback.message.answer(
                text=f"❌ Error <code>{username}</code> Create!"
            )

    await callback.message.delete()
    await state.clear()
    new_message = await callback.message.answer(
        text=MessageTexts.START, reply_markup=BotKeyboards.home()
    )
    return await storage.clear_and_add_message(new_message)
