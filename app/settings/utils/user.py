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
from app.api.types.marzban import MarzbanProxyInbound, MarzbanUserResponse
from app.api.types.marzneshin import MarzneshinUserResponse


def _get_expire_strategy(types: ServerTypes, datetype: str):
    if types == ServerTypes.MARZNESHIN.value:
        return {
            DateTypes.NOW.value: MarzneshinUserExpireStrategy.FIXED_DATE,
            DateTypes.AFTER_FIRST_USE.value: MarzneshinUserExpireStrategy.START_ON_FIRST_USE,
            DateTypes.UNLIMITED.value: MarzneshinUserExpireStrategy.NEVER,
        }.get(datetype)
    elif types == ServerTypes.MARZBAN.value:
        return {
            DateTypes.NOW.value: MarzbanUserStatus.ACTIVE,
            DateTypes.AFTER_FIRST_USE.value: MarzbanUserStatus.ONHOLD,
            DateTypes.UNLIMITED.value: MarzbanUserStatus.ACTIVE,
        }.get(datetype)
    return None


def _get_expire_date(expire_strategy, datelimit: int):
    if expire_strategy in [
        MarzneshinUserExpireStrategy.FIXED_DATE,
        MarzbanUserStatus.ACTIVE,
    ]:
        return (
            datetime.utcnow() + timedelta(days=int(datelimit))
            if int(datelimit) != 0
            else 0
        )
    return None


def _get_usage_duration(expire_strategy, datelimit: int):
    if expire_strategy in [
        MarzneshinUserExpireStrategy.START_ON_FIRST_USE,
        MarzbanUserStatus.ONHOLD,
    ]:
        return int(datelimit) * (24 * 60 * 60)
    return None


def _get_proxies_and_inbounds(configs: dict | None = None):
    if not configs:
        return {}, {}
    inbound_objects = [MarzbanProxyInbound(**item) for item in configs]
    proxies = {
        proto: {} for proto in {inbound.protocol.value for inbound in inbound_objects}
    }
    inbounds = {
        proto: [
            inbound.tag
            for inbound in inbound_objects
            if inbound.protocol.value == proto
        ]
        for proto in proxies
    }
    return proxies, inbounds


def user_create_data(
    types: ServerTypes,
    username: str,
    datalimit: int,
    datetype: str,
    datelimit: int,
    selects: dict,
) -> dict:
    expire_strategy = _get_expire_strategy(types, datetype)
    expire_date = _get_expire_date(expire_strategy, datelimit)
    usage_duration = _get_usage_duration(expire_strategy, datelimit)
    datalimit = int(datalimit)
    if types == ServerTypes.MARZNESHIN.value:
        data = MarzneshinUserCreate(
            username=username,
            data_limit=datalimit * (1024**3) if datalimit != 0 else 0,
            service_ids=[service["id"] for service in selects],
            expire_strategy=expire_strategy,
            expire_date=expire_date,
            usage_duration=usage_duration,
        ).dict()
    elif types == ServerTypes.MARZBAN.value:
        proxies, inbounds = _get_proxies_and_inbounds(selects)
        data = MarzbanUserCreate(
            username=username,
            data_limit=datalimit * (1024**3) if datalimit != 0 else 0,
            inbounds=inbounds,
            proxies=proxies,
            status=expire_strategy,
            expire=int(expire_date.timestamp()) if expire_date else None,
            on_hold_expire_duration=usage_duration
            if expire_strategy == MarzbanUserStatus.ONHOLD
            else None,
        ).dict()
    return data


def charge_user_data(
    types: ServerTypes,
    user: MarzbanUserResponse | MarzneshinUserResponse,
    datalimit: int,
    datelimit: int,
    datetypes: str,
    charge: bool = False,
) -> dict:
    if charge:
        return advenced_charge_user_data(types, user, datalimit, datelimit, datetypes)
    return normal_charge_user_data(types, user, datalimit, datelimit, datetypes)


def advenced_charge_user_data(
    types: ServerTypes,
    user: MarzbanUserResponse | MarzneshinUserResponse,
    datalimit: int,
    datelimit: int,
    datetypes: str,
) -> dict:
    match types:
        case ServerTypes.MARZBAN:
            data = MarzbanUserModify(
                data_limit=int(datalimit) * (1024**3) + user.data_limit
                if user.data_limit
                else 0,
                status="on_hold"
                if datetypes == DateTypes.AFTER_FIRST_USE
                else "active",
                expire=int(
                    int((datelimit) * (24 * 60 * 60)) + (user.expire or datetime.now())
                )
                if datetypes != DateTypes.AFTER_FIRST_USE
                else None,
                on_hold_expire_duration=int(
                    int((datelimit) * (24 * 60 * 60))
                    + (user.on_hold_expire_duration or 0)
                )
                if datetypes == DateTypes.AFTER_FIRST_USE
                else None,
            ).dict()
        case ServerTypes.MARZNESHIN:
            expire_strategy = _get_expire_strategy(types, datetypes)
            data = MarzneshinUserModify(
                username=user.username,
                data_limit=int(datalimit) * (1024**3) + user.data_limit
                if user.data_limit
                else 0,
                expire_strategy=expire_strategy,
                expire_date=timedelta(
                    seconds=user.time_to_second + int(datelimit * (24 * 60 * 60))
                )
                if expire_strategy == MarzneshinUserExpireStrategy.FIXED_DATE
                else None,
                usage_duration=user.time_to_second + (int(datelimit) * (24 * 60 * 60))
                if expire_strategy == MarzneshinUserExpireStrategy.START_ON_FIRST_USE
                else None,
            ).dict()

    return data


def normal_charge_user_data(
    types: ServerTypes,
    user: MarzbanUserResponse | MarzneshinUserResponse,
    datalimit: int,
    datelimit: int,
    status: str,
) -> dict:
    expire_strategy = _get_expire_strategy(types, status)
    expire_date = _get_expire_date(expire_strategy, datelimit)
    usage_duration = _get_usage_duration(expire_strategy, datelimit)

    if types == ServerTypes.MARZBAN.value:
        data = MarzbanUserModify(
            data_limit=int(datalimit) * (1024**3),
            status=expire_strategy,
            expire=int(expire_date.timestamp())
            if expire_date
            else (0 if status == DateTypes.UNLIMITED else None),
            on_hold_expire_duration=usage_duration
            if expire_strategy == MarzbanUserStatus.ONHOLD
            else None,
        ).dict()
    elif types == ServerTypes.MARZNESHIN.value:
        data = MarzneshinUserModify(
            username=user.username,
            data_limit=int(datalimit) * (1024**3),
            expire_strategy=expire_strategy,
            expire_date=expire_date,
            usage_duration=usage_duration,
        ).dict()
    return data


def change_config_data(types: str, username: str, configs: dict, selects: dict) -> dict:
    if types == ServerTypes.MARZBAN.value:
        proxies, inbounds = _get_proxies_and_inbounds(configs)
        data = MarzbanUserModify(
            inbounds=inbounds,
            proxies=proxies,
        ).dict()
    elif types == ServerTypes.MARZNESHIN.value:
        data = MarzneshinUserModify(
            username=username,
            service_ids=[int(service["id"]) for service in selects],
        ).dict()
    return data


def update_user_data_limit_data(
    types: ServerTypes, username: str, datalimit: int
) -> dict:
    data_limit = int(datalimit) * (1024**3)
    if types == ServerTypes.MARZBAN.value:
        data = MarzbanUserModify(data_limit=data_limit).dict()
    elif types == ServerTypes.MARZNESHIN.value:
        data = MarzneshinUserModify(username=username, data_limit=data_limit).dict()
    return data


def charge_user_datelimit(
    types: ServerTypes, username: str, datelimit: int, status: str
) -> dict:
    expire_strategy = _get_expire_strategy(types, status)
    expire_date = _get_expire_date(expire_strategy, datelimit)
    usage_duration = _get_usage_duration(expire_strategy, datelimit)

    if types == ServerTypes.MARZBAN.value:
        data = MarzbanUserModify(
            status=expire_strategy,
            expire=int(expire_date.timestamp())
            if expire_date
            else (0 if status == DateTypes.UNLIMITED else None),
            on_hold_expire_duration=usage_duration
            if expire_strategy == MarzbanUserStatus.ONHOLD
            else None,
        ).dict()
    elif types == ServerTypes.MARZNESHIN.value:
        data = MarzneshinUserModify(
            username=username,
            expire_strategy=expire_strategy,
            expire_date=expire_date,
            usage_duration=usage_duration,
        ).dict()
    return data
