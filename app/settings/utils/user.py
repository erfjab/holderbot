from datetime import datetime, timedelta
from app.models.user import (
    MarzneshinUserCreate,
    MarzneshinUserExpireStrategy,
    DateTypes,
    MarzbanUserStatus,
    MarzbanUserCreate,
    MarzbanUserModify,
    MarzneshinUserModify,
)
from app.models.server import ServerTypes
from app.api.types.marzban import MarzbanProxyInbound


def user_create_data(
    types: ServerTypes,
    username: str,
    datalimit: int,
    datetype: MarzneshinUserExpireStrategy,
    datelimit: int,
    selects: dict,
    configs: dict | None = None,
) -> dict:
    match types:
        case ServerTypes.MARZNESHIN.value:
            datatypesfind = {
                DateTypes.NOW.value: MarzneshinUserExpireStrategy.FIXED_DATE,
                DateTypes.AFTER_FIRST_USE.value: MarzneshinUserExpireStrategy.START_ON_FIRST_USE,
                DateTypes.UNLIMITED.value: MarzneshinUserExpireStrategy.NEVER,
            }
            datetype = datatypesfind.get(datetype)
            data = MarzneshinUserCreate(
                username=username,
                data_limit=int(int(datalimit) * (1024**3)),
                service_ids=[service["id"] for service in selects],
                expire_strategy=datetype,
                expire_date=(datetime.utcnow() + timedelta(days=datelimit))
                if datetype == MarzneshinUserExpireStrategy.FIXED_DATE
                else None,
                usage_duration=(datelimit * (24 * 60 * 60))
                if datetype == MarzneshinUserExpireStrategy.START_ON_FIRST_USE
                else None,
            ).dict()

        case ServerTypes.MARZBAN.value:
            datatypesfind = {
                DateTypes.NOW.value: MarzbanUserStatus.ACTIVE,
                DateTypes.AFTER_FIRST_USE.value: MarzbanUserStatus.ONHOLD,
                DateTypes.UNLIMITED.value: MarzbanUserStatus.ACTIVE,
            }
            datetype = datatypesfind.get(datetype)
            inbound_objects = [MarzbanProxyInbound(**item) for item in configs]
            proxies = {
                proto: {}
                for proto in {inbound.protocol.value for inbound in inbound_objects}
            }
            inbounds = {
                proto: [
                    inbound.tag
                    for inbound in inbound_objects
                    if inbound.protocol.value == proto
                ]
                for proto in proxies
            }
            data = MarzbanUserCreate(
                username=username,
                data_limit=int(int(datalimit) * (1024**3)),
                inbounds=inbounds,
                proxies=proxies,
                status=datetype,
                expire=int((datetime.utcnow() + timedelta(days=datelimit)).timestamp())
                if datetype == MarzbanUserStatus.ACTIVE
                else None,
                on_hold_expire_duration=int(datelimit * (24 * 60 * 60))
                if datetype == MarzbanUserStatus.ONHOLD
                else None,
            ).dict()

    return data


def charge_user_data(
    types: ServerTypes, username: str, datalimit: int, datelimit: int, status: str
) -> dict:
    match types:
        case ServerTypes.MARZBAN.value:
            datatypesfind = {
                DateTypes.NOW.value: MarzbanUserStatus.ACTIVE,
                DateTypes.AFTER_FIRST_USE.value: MarzbanUserStatus.ONHOLD,
                DateTypes.UNLIMITED.value: MarzbanUserStatus.ACTIVE,
            }
            datetype = datatypesfind.get(status)
            datelimit = int(datelimit)
            data = MarzbanUserModify(
                data_limit=int(datalimit) * (1024**3),
                status=datetype,
                expire=int((datetime.utcnow() + timedelta(days=datelimit)).timestamp())
                if datetype == MarzbanUserStatus.ACTIVE
                else 0
                if status == DateTypes.UNLIMITED
                else None,
                on_hold_expire_duration=int(datelimit * (24 * 60 * 60))
                if datetype == MarzbanUserStatus.ONHOLD
                else None,
            ).dict()
        case ServerTypes.MARZNESHIN.value:
            datatypesfind = {
                DateTypes.NOW.value: MarzneshinUserExpireStrategy.FIXED_DATE,
                DateTypes.AFTER_FIRST_USE.value: MarzneshinUserExpireStrategy.START_ON_FIRST_USE,
                DateTypes.UNLIMITED.value: MarzneshinUserExpireStrategy.NEVER,
            }
            datetype = datatypesfind.get(status)
            datelimit = int(datelimit)
            data = MarzneshinUserModify(
                username=username,
                data_limit=int(datalimit) * (1024**3),
                expire_strategy=datetype,
                expire_date=(datetime.utcnow() + timedelta(days=datelimit))
                if datetype == MarzneshinUserExpireStrategy.FIXED_DATE
                else None,
                usage_duration=(datelimit * (24 * 60 * 60))
                if datetype == MarzneshinUserExpireStrategy.START_ON_FIRST_USE
                else None,
            ).dict()
    return data


def change_config_data(types: str, username: str, configs: dict, selects: dict) -> dict:
    match types:
        case ServerTypes.MARZBAN.value:
            inbound_objects = [MarzbanProxyInbound(**item) for item in configs]
            proxies = {
                proto: {}
                for proto in {inbound.protocol.value for inbound in inbound_objects}
            }
            inbounds = {
                proto: [
                    inbound.tag
                    for inbound in inbound_objects
                    if inbound.protocol.value == proto
                ]
                for proto in proxies
            }
            data = MarzbanUserModify(
                inbounds=inbounds,
                proxies=proxies,
            ).dict()
        case ServerTypes.MARZNESHIN.value:
            data = MarzneshinUserModify(
                username=username,
                service_ids=[int(service["id"]) for service in selects],
            ).dict()
    return data


def update_user_data_limit_data(
    types: ServerTypes, username: str, datalimit: int
) -> dict:
    match types:
        case ServerTypes.MARZBAN.value:
            data = MarzbanUserModify(data_limit=int(datalimit) * (1024**3)).dict()
        case ServerTypes.MARZNESHIN.value:
            data = MarzneshinUserModify(
                username=username, data_limit=int(datalimit) * (1024**3)
            ).dict()
    return data


def charge_user_datelimit(
    types: ServerTypes, username: str, datelimit: int, status: str
) -> dict:
    match types:
        case ServerTypes.MARZBAN.value:
            datatypesfind = {
                DateTypes.NOW.value: MarzbanUserStatus.ACTIVE,
                DateTypes.AFTER_FIRST_USE.value: MarzbanUserStatus.ONHOLD,
                DateTypes.UNLIMITED.value: MarzbanUserStatus.ACTIVE,
            }
            datetype = datatypesfind.get(status)
            datelimit = int(datelimit)
            data = MarzbanUserModify(
                status=datetype,
                expire=int((datetime.utcnow() + timedelta(days=datelimit)).timestamp())
                if datetype == MarzbanUserStatus.ACTIVE
                else 0
                if status == DateTypes.UNLIMITED
                else None,
                on_hold_expire_duration=int(datelimit * (24 * 60 * 60))
                if datetype == MarzbanUserStatus.ONHOLD
                else None,
            ).dict()
        case ServerTypes.MARZNESHIN.value:
            datatypesfind = {
                DateTypes.NOW.value: MarzneshinUserExpireStrategy.FIXED_DATE,
                DateTypes.AFTER_FIRST_USE.value: MarzneshinUserExpireStrategy.START_ON_FIRST_USE,
                DateTypes.UNLIMITED.value: MarzneshinUserExpireStrategy.NEVER,
            }
            datetype = datatypesfind.get(status)
            datelimit = int(datelimit)
            data = MarzneshinUserModify(
                username=username,
                expire_strategy=datetype,
                expire_date=(datetime.utcnow() + timedelta(days=datelimit))
                if datetype == MarzneshinUserExpireStrategy.FIXED_DATE
                else None,
                usage_duration=(datelimit * (24 * 60 * 60))
                if datetype == MarzneshinUserExpireStrategy.START_ON_FIRST_USE
                else None,
            ).dict()
    return data
