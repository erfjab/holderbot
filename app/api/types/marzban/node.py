from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MarzbanNodeStatus(str, Enum):
    connected = "connected"
    connecting = "connecting"
    error = "error"
    disabled = "disabled"


class MarzbanNode(BaseModel):
    name: str
    address: str
    port: int = 62050
    api_port: int = 62051
    usage_coefficient: float = Field(gt=0, default=1.0)


class MarzbanNodeResponse(MarzbanNode):
    id: int
    xray_version: Optional[str] = None
    status: MarzbanNodeStatus
    message: Optional[str] = None

    @property
    def is_have_error(self) -> bool:
        return self.status in [MarzbanNodeStatus.connecting, MarzbanNodeStatus.error]

    @property
    def remark(self) -> bool:
        return self.name
