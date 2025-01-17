from enum import Enum
from typing import Union

from pydantic import BaseModel


class MarzbanProxyTypes(str, Enum):
    VMess = "vmess"
    VLESS = "vless"
    Trojan = "trojan"
    Shadowsocks = "shadowsocks"


class MarzbanProxyInbound(BaseModel):
    tag: str
    protocol: MarzbanProxyTypes
    network: str
    tls: str
    port: Union[int, str]

    @property
    def remark(self):
        return self.tag

    @property
    def name(self):
        return self.tag

    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        base_dict["name"] = self.name
        return base_dict
