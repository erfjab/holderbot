from enum import Enum


class ServerTypes(str, Enum):
    MARZNESHIN = "marzneshin"
    MARZBAN = "marzban"


class ServerModify(str, Enum):
    REMOVE = "🗑 Remove"
    REMARK = "🏷 Remark"
    DATA = "📋 Data"
