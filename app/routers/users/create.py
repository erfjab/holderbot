import asyncio
import json
from secrets import token_hex

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keys import (
    BotKeys,
    PageCB,
    Pages,
    Actions,
    SelectCB,
    SelectAll,
    JsonHandler,
    RandomHandler,
)
from app.db import crud
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.models.user import DateTypes, UserJsonData
from app.settings.utils.qrcode import create_qr
from app.settings.track import tracker
from app.settings.log import logger
from app.settings.utils.user import user_create_data


class UserCreateForm(StatesGroup):
    ADMIN = State()
    USERNAME = State()
    USERCOUNT = State()
    USERSUFFIX = State()
    TEMPLATE = State()
    DATA_LIMIT = State()
    DATE_TYPE = State()
    DATE_LIMIT = State()
    CONFIGS = State()
    JSON = State()


router = Router(name="users_create")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.USERS)) & (F.action.is_(Actions.CREATE)))
)
async def data(callback: CallbackQuery, callback_data: PageCB, state: FSMContext):
    server = await crud.get_server(callback_data.panel)
    if not server:
        await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )

    await state.set_state(UserCreateForm.ADMIN)
    await state.update_data(panel=callback_data.panel)
    admins = await ClinetManager.get_admins(server=server)
    if not admins:
        await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )

    return await callback.message.edit_text(
        text=MessageTexts.ASK_ADMIN,
        reply_markup=BotKeys.selector(
            data=[admin.username for admin in admins],
            types=Pages.USERS,
            action=Actions.CREATE,
            panel=server.id,
            server_back=server.id,
        ),
    )


@router.callback_query(
    StateFilter(UserCreateForm.ADMIN),
    SelectCB.filter((F.types.is_(Pages.USERS)) & (F.action.is_(Actions.CREATE))),
)
async def adminselect(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    await state.set_state(UserCreateForm.USERNAME)
    await state.update_data(admin=callback_data.select)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_REMARK,
        reply_markup=BotKeys.selector(
            data=[
                (MessageTexts.RANDOM_USERNAME, RandomHandler.USERNAME),
                (MessageTexts.CREATE_WITH_JSON, JsonHandler.USER),
            ],
            types=Pages.USERS,
            action=Actions.JSON,
            panel=callback_data.panel,
            width=1,
            server_back=int(await state.get_value("panel")),
        ),
    )


@router.callback_query(
    StateFilter(UserCreateForm.USERNAME),
    SelectCB.filter((F.types.is_(Pages.USERS)) & (F.action.is_(Actions.JSON))),
)
async def json_start(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    if callback_data.select == JsonHandler.USER:
        await state.set_state(UserCreateForm.JSON)
        text = MessageTexts.ASK_JSON
    else:
        await state.update_data(username=str(token_hex(3)))
        await state.set_state(UserCreateForm.USERCOUNT)
        text = MessageTexts.ASK_COUNT
    return await callback.message.edit_text(
        text=text,
        reply_markup=BotKeys.cancel(server_back=int(await state.get_value("panel"))),
    )


@router.message(StateFilter(UserCreateForm.JSON))
async def json_input(message: Message, state: FSMContext):
    if not message.document:
        track = await message.answer(text=MessageTexts.WORNG_DOC)
        return await tracker.add(track)

    if not message.document.file_name.endswith(".json"):
        track = await message.answer(text=MessageTexts.WORNG_JSON)
        return await tracker.add(track)

    try:
        file = await message.bot.get_file(message.document.file_id)
        file_content = await message.bot.download_file(file.file_path)
        json_str = file_content.getvalue().decode("utf-8")
        json_data = json.loads(json_str)
        validated_users = [UserJsonData.model_validate(user) for user in json_data]
        await state.update_data(
            uploaded_json=[user.to_dict() for user in validated_users]
        )
        await state.set_state(UserCreateForm.CONFIGS)
        serverid = int(await state.get_value("panel"))
        server = await crud.get_server(serverid)
        if not server:
            track = await message.answer(
                text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
            )
            return await tracker.cleardelete(message, track)

        configs = await ClinetManager.get_configs(server)
        if not configs:
            track = await message.answer(
                text=MessageTexts.NOT_FOUND,
                reply_markup=BotKeys.cancel(server_back=serverid),
            )
            return await tracker.cleardelete(message, track)

        await state.update_data(configs=[config.dict() for config in configs])
        await state.update_data(selects=[config.dict() for config in configs])
        track = await message.answer(
            text=MessageTexts.ASK_CONFIGS,
            reply_markup=BotKeys.selector(
                data=[config.name for config in configs],
                types=Pages.USERS,
                action=Actions.CREATE,
                selects=[config.name for config in configs],
                panel=server.id,
                all_selects=True,
                server_back=serverid,
            ),
        )
        return await tracker.cleardelete(message, track)
    except Exception as e:
        logger.info(f"Error in json read: {str(e)}")
        track = await message.answer(text=MessageTexts.INVALID_JSON)
        await tracker.add(track)


@router.message(StateFilter(UserCreateForm.USERNAME))
async def username(message: Message, state: FSMContext):
    if len(message.text) <= 3:
        track = await message.answer(text=MessageTexts.WRONG_PATTERN)
        return await tracker.add(track)

    await state.update_data(username=message.text)
    await state.set_state(UserCreateForm.USERCOUNT)
    track = await message.answer(
        text=MessageTexts.ASK_COUNT,
        reply_markup=BotKeys.cancel(int(await state.get_value("panel"))),
    )
    return await tracker.cleardelete(message, track)


@router.message(StateFilter(UserCreateForm.USERCOUNT))
async def usercount(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 1:
        track = await message.answer(text=MessageTexts.WRONG_INT)
        return await tracker.add(track)
    serverid = int(await state.get_value("panel"))
    await state.update_data(usercount=message.text)
    if int(message.text) == 1:
        templates = await crud.get_templates(active=True)
        if templates:
            await state.set_state(UserCreateForm.TEMPLATE)
            track = await message.answer(
                text=MessageTexts.ITEMS,
                reply_markup=BotKeys.selector(
                    data=[tem.button_remark for tem in templates] + ["CUSTOM"],
                    types=Pages.USERS,
                    action=Actions.CREATE,
                    width=1,
                    server_back=serverid,
                ),
            )
            return await tracker.cleardelete(message, track)
        await state.set_state(UserCreateForm.DATA_LIMIT)
        text = MessageTexts.ASK_DATA_LIMT
    else:
        await state.set_state(UserCreateForm.USERSUFFIX)
        text = MessageTexts.ASK_SUFFIX

    track = await message.answer(
        text=text, reply_markup=BotKeys.cancel(server_back=serverid)
    )
    return await tracker.cleardelete(message, track)


@router.message(StateFilter(UserCreateForm.USERSUFFIX))
async def userprefix(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 1:
        track = await message.answer(text=MessageTexts.WRONG_INT)
        return await tracker.add(track)
    serverid = int(await state.get_value("panel"))
    await state.update_data(usersuffix=message.text)
    templates = await crud.get_templates(active=True)
    if not templates:
        await state.set_state(UserCreateForm.DATA_LIMIT)
        track = await message.answer(
            text=MessageTexts.ASK_DATA_LIMT,
            reply_markup=BotKeys.cancel(server_back=serverid),
        )
        return await tracker.cleardelete(message, track)

    await state.set_state(UserCreateForm.TEMPLATE)
    track = await message.answer(
        text=MessageTexts.ITEMS,
        reply_markup=BotKeys.selector(
            data=[tem.button_remark for tem in templates] + ["CUSTOM"],
            types=Pages.USERS,
            action=Actions.CREATE,
            width=1,
            server_back=serverid,
        ),
    )
    await tracker.cleardelete(message, track)


@router.callback_query(
    StateFilter(UserCreateForm.TEMPLATE),
    SelectCB.filter((F.types.is_(Pages.USERS)) & (F.action.is_(Actions.CREATE))),
)
async def templateselect(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    panelid = int(await state.get_value("panel"))
    if callback_data.select == "CUSTOM":
        await state.set_state(UserCreateForm.DATA_LIMIT)
        track = await callback.message.answer(
            text=MessageTexts.ASK_DATA_LIMT,
            reply_markup=BotKeys.cancel(server_back=panelid),
        )
        return await tracker.cleardelete(callback, track)
    template = await crud.get_template(int(callback_data.select.split()[0]))
    if not template:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=panelid),
        )
        return await tracker.add(track)

    await state.update_data(datalimit=template.data_limit)
    await state.update_data(datelimit=template.date_limit)
    await state.update_data(datetypes=template.date_types)

    await state.set_state(UserCreateForm.CONFIGS)
    server = await crud.get_server(panelid)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    configs = await ClinetManager.get_configs(server)
    if not configs:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )
        return await tracker.add(track)

    await state.update_data(configs=[config.dict() for config in configs])
    await state.update_data(selects=[config.dict() for config in configs])
    return await callback.message.edit_text(
        text=MessageTexts.ASK_CONFIGS,
        reply_markup=BotKeys.selector(
            data=[config.name for config in configs],
            types=Pages.USERS,
            action=Actions.CREATE,
            selects=[config.name for config in configs],
            panel=server.id,
            all_selects=True,
            server_back=server.id,
        ),
    )


@router.message(StateFilter(UserCreateForm.DATA_LIMIT))
async def datalimit(message: Message, state: FSMContext):
    if not message.text.isdigit():
        track = await message.answer(text=MessageTexts.WRONG_INT)
        return await tracker.add(track)

    await state.update_data(datalimit=message.text)
    await state.set_state(UserCreateForm.DATE_TYPE)
    serverid = await state.get_value("panel")
    track = await message.answer(
        text=MessageTexts.MENU,
        reply_markup=BotKeys.selector(
            data=[DateTypes.UNLIMITED, DateTypes.NOW, DateTypes.AFTER_FIRST_USE],
            types=Pages.USERS,
            action=Actions.CREATE,
            width=1,
            panel=serverid,
            server_back=serverid,
        ),
    )
    return await tracker.cleardelete(message, track)


@router.callback_query(
    StateFilter(UserCreateForm.DATE_TYPE),
    SelectCB.filter((F.types.is_(Pages.USERS)) & (F.action.is_(Actions.CREATE))),
)
async def datetypes(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.update_data(datetypes=callback_data.select)
    if callback_data.select == DateTypes.UNLIMITED.value:
        await state.set_state(UserCreateForm.CONFIGS)
        await state.update_data(datelimit=0)
        configs = await ClinetManager.get_configs(server)
        if not configs:
            track = await callback.message.edit_text(
                text=MessageTexts.NOT_FOUND,
                reply_markup=BotKeys.cancel(server_back=server.id),
            )
            return await tracker.add(track)

        await state.update_data(configs=[config.dict() for config in configs])
        await state.update_data(selects=[config.dict() for config in configs])
        return await callback.message.edit_text(
            text=MessageTexts.ASK_CONFIGS,
            reply_markup=BotKeys.selector(
                data=[config.name for config in configs],
                types=Pages.USERS,
                action=Actions.CREATE,
                selects=[config.name for config in configs],
                panel=server.id,
                all_selects=True,
                server_back=server.id,
            ),
        )
    else:
        await state.set_state(UserCreateForm.DATE_LIMIT)
        return await callback.message.edit_text(
            text=MessageTexts.ASK_DATE_LIMIT,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )


@router.message(StateFilter(UserCreateForm.DATE_LIMIT))
async def datelimit(message: Message, state: FSMContext):
    if not message.text.isdigit():
        track = await message.answer(text=MessageTexts.WRONG_INT)
        return await tracker.add(track)

    server = await crud.get_server(await state.get_value("panel"))
    if not server:
        track = await message.answer(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.update_data(datelimit=message.text)
    await state.set_state(UserCreateForm.CONFIGS)
    configs = await ClinetManager.get_configs(server)
    if not configs:
        track = await message.answer(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )
        return await tracker.add(track)

    await state.update_data(configs=[config.dict() for config in configs])
    await state.update_data(selects=[config.dict() for config in configs])
    track = await message.answer(
        text=MessageTexts.ASK_CONFIGS,
        reply_markup=BotKeys.selector(
            data=[config.name for config in configs],
            types=Pages.USERS,
            action=Actions.CREATE,
            selects=[config.name for config in configs],
            panel=server.id,
            all_selects=True,
            server_back=server.id,
        ),
    )
    return await tracker.cleardelete(message, track)


@router.callback_query(
    StateFilter(UserCreateForm.CONFIGS),
    SelectCB.filter(
        (F.types.is_(Pages.USERS))
        & (F.action.is_(Actions.CREATE))
        & (F.done.is_(False))
    ),
)
async def configs(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    data = await state.get_data()
    configs = data["configs"]
    selected = callback_data.select
    selects = data["selects"]

    if selected in [SelectAll.SELECT, SelectAll.DESELECT]:
        if selected == SelectAll.SELECT:
            selects = [config for config in configs]
        elif selected == SelectAll.DESELECT:
            selects = []
    else:
        if selected in {select["name"] for select in selects}:
            selects = [select for select in selects if select["name"] != selected]
        else:
            target_config = next(
                config for config in configs if config["name"] == selected
            )
            selects.append(target_config)

    await state.update_data(selects=selects)

    return await callback.message.edit_text(
        text=MessageTexts.ASK_CONFIGS,
        reply_markup=BotKeys.selector(
            data=[config["name"] for config in configs],
            types=Pages.USERS,
            action=Actions.CREATE,
            selects=[select["name"] for select in selects],
            panel=data["panel"],
            all_selects=True,
            server_back=data["panel"],
        ),
    )


@router.callback_query(
    StateFilter(UserCreateForm.CONFIGS),
    SelectCB.filter(
        (F.types.is_(Pages.USERS)) & (F.action.is_(Actions.CREATE)) & (F.done.is_(True))
    ),
)
async def createusers(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    data = await state.get_data()

    configs = data["selects"]
    if not configs:
        return await callback.answer(
            text=MessageTexts.NOT_FOUND_CONFIGS, show_alert=True
        )

    server = await crud.get_server(int(callback_data.panel))
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.cleardelete(callback, track)
    users = data.get("uploaded_json", None)
    if users:
        for user in users:
            user_data = user_create_data(
                server.types,
                username=user["username"],
                datalimit=int(user["datalimit"]),
                datetype=user["datetypes"],
                datelimit=int(user["datelimit"]),
                selects=data["selects"],
            )
            user_created = await ClinetManager.create_user(server, user_data)
            if not user_created:
                await callback.message.answer(
                    text=MessageTexts.FAILED_USERNAME.format(username=user["username"]),
                )
            else:
                await ClinetManager.set_owner(
                    server=server, username=user_created.username, admin=data["admin"]
                )
                await callback.message.answer_photo(
                    photo=BufferedInputFile(
                        await create_qr(user_created.subscription_url),
                        filename="holderbot.png",
                    ),
                    caption=MessageTexts.USER_INFO.format(**user_created.format_data),
                )
            await asyncio.sleep(0.5)
    else:
        for i in range(int(data["usercount"])):
            username = (
                f"{data['username']}{i + int(data['usersuffix'])}"
                if data.get("usersuffix")
                else data["username"]
            )
            user_data = user_create_data(
                server.types,
                username=username,
                datalimit=int(data["datalimit"]),
                datetype=data["datetypes"],
                datelimit=int(data["datelimit"]),
                selects=data["selects"],
            )
            user_created = await ClinetManager.create_user(server, user_data)
            if not user_created:
                await callback.message.answer(
                    text=MessageTexts.FAILED_USERNAME.format(username=username),
                )
            else:
                await ClinetManager.set_owner(
                    server=server, username=user_created.username, admin=data["admin"]
                )
                await callback.message.answer_photo(
                    photo=BufferedInputFile(
                        await create_qr(user_created.subscription_url),
                        filename="holderbot.png",
                    ),
                    caption=MessageTexts.USER_INFO.format(**user_created.format_data),
                )
            await asyncio.sleep(0.5)

    await state.clear()
    track = await callback.message.answer(
        text=MessageTexts.LETS_BACK,
        reply_markup=BotKeys.cancel(server_back=data["panel"]),
    )
    return await tracker.cleardelete(callback, track)
