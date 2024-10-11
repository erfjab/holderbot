from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from marzban import ProxyInbound

from utils.lang import MessageTexts
from utils.keys import BotKeyboards
from utils.statedb import storage
from utils import panel, text_info, helpers
from models import (
    PagesActions,
    PagesCallbacks,
    AdminActions,
    UserCreateForm,
    UserStatusCallbacks,
    UserInboundsCallbacks,
)


router = Router()


@router.callback_query(PagesCallbacks.filter(F.page.is_(PagesActions.UserCreate)))
async def user_create(
    callback: CallbackQuery, callback_data: PagesCallbacks, state: FSMContext
):
    await state.set_state(UserCreateForm.base_username)
    return await callback.message.edit_text(
        text=MessageTexts.AskCreateUserBaseUsername, reply_markup=BotKeyboards.cancel()
    )


@router.message(StateFilter(UserCreateForm.base_username))
async def user_create_base_username(message: Message, state: FSMContext):
    await state.update_data(base_username=message.text)
    await state.set_state(UserCreateForm.start_number)
    new_message = await message.answer(
        text=MessageTexts.AskCreateUserStartNumber, reply_markup=BotKeyboards.cancel()
    )
    return await storage.clear_and_add_message(new_message)


@router.message(StateFilter(UserCreateForm.start_number))
async def user_create_start_number(message: Message, state: FSMContext):

    if not message.text.isdigit():
        new_message = await message.answer(text=MessageTexts.JustNumber)
        return await storage.add_log_message(
            message.from_user.id, new_message.message_id
        )

    await state.update_data(start_number=int(message.text))
    await state.set_state(UserCreateForm.how_much)
    new_message = await message.answer(
        text=MessageTexts.AskCreateUserHowMuch, reply_markup=BotKeyboards.cancel()
    )
    return await storage.clear_and_add_message(new_message)


@router.message(StateFilter(UserCreateForm.how_much))
async def user_create_how_much(message: Message, state: FSMContext):

    if not message.text.isdigit():
        new_message = await message.answer(text=MessageTexts.JustNumber)
        return await storage.add_log_message(
            message.from_user.id, new_message.message_id
        )

    await state.update_data(how_much=int(message.text))
    await state.set_state(UserCreateForm.data_limit)
    new_message = await message.answer(
        text=MessageTexts.AskCreateUserDataLimit, reply_markup=BotKeyboards.cancel()
    )
    return await storage.clear_and_add_message(new_message)


@router.message(StateFilter(UserCreateForm.data_limit))
async def user_create_data_limit(message: Message, state: FSMContext):

    if not message.text.isdigit():
        new_message = await message.answer(text=MessageTexts.JustNumber)
        return await storage.add_log_message(
            message.from_user.id, new_message.message_id
        )

    await state.update_data(data_limit=int(message.text))
    await state.set_state(UserCreateForm.date_limit)
    new_message = await message.answer(
        text=MessageTexts.AskCreateUserDateLimit, reply_markup=BotKeyboards.cancel()
    )
    return await storage.clear_and_add_message(new_message)


@router.message(StateFilter(UserCreateForm.date_limit))
async def user_create_date_limit(message: Message, state: FSMContext):

    if not message.text.isdigit():
        new_message = await message.answer(text=MessageTexts.JustNumber)
        return await storage.add_log_message(
            message.from_user.id, new_message.message_id
        )

    await state.update_data(date_limit=int(message.text))
    new_message = await message.answer(
        text=MessageTexts.AskCreateUserStatus,
        reply_markup=BotKeyboards.user_status(AdminActions.Add),
    )
    return await storage.clear_and_add_message(new_message)


@router.callback_query(UserStatusCallbacks.filter(F.action.is_(AdminActions.Add)))
async def user_create_status(
    callback: CallbackQuery, callback_data: UserStatusCallbacks, state: FSMContext
):
    await state.update_data(status=callback_data.status)
    inbounds = await panel.inbounds()
    await state.update_data(inbounds=inbounds)
    return await callback.message.edit_text(
        text=MessageTexts.AskCreateUserInbouds,
        reply_markup=BotKeyboards.inbounds(inbounds),
    )


@router.callback_query(
    UserInboundsCallbacks.filter(
        (F.action.is_(AdminActions.Add) & (F.is_done.is_(False)))
    )
)
async def user_create_inbounds(
    callback: CallbackQuery,
    callback_data: UserInboundsCallbacks,
    state: FSMContext,
):
    data = await state.get_data()
    inbounds = data.get("inbounds")
    selected_inbounds = set(data.get("selected_inbounds", []))
    (
        selected_inbounds.add(callback_data.tag)
        if callback_data.is_selected is False
        else selected_inbounds.discard(callback_data.tag)
    )
    await state.update_data(selected_inbounds=list(selected_inbounds))
    await callback.message.edit_reply_markup(
        reply_markup=BotKeyboards.inbounds(inbounds, selected_inbounds)
    )


@router.callback_query(
    UserInboundsCallbacks.filter(
        (F.action.is_(AdminActions.Add) & (F.is_done.is_(True)))
    )
)
async def user_create_inbounds_save(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    inbounds: dict[str, list[ProxyInbound]] = data.get("inbounds")
    selected_inbounds = set(data.get("selected_inbounds", []))

    if not selected_inbounds:
        return await callback.answer(
            text=MessageTexts.NoneUserInbounds, show_alert=True
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
            qr_bytes = await helpers.create_qr(new_user.subscription_url)
            await callback.message.answer_photo(
                caption=text_info.user_info(new_user),
                photo=BufferedInputFile(qr_bytes, filename="qr_code.png"),
            )
        else:
            await callback.message.answer(
                text=f"❌ Error <code>{username}</code> Create!"
            )

    await callback.message.delete()
