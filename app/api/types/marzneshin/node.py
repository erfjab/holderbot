from enum import Enum

from pydantic import BaseModel, Field


class MarzneshinBackend(BaseModel):
    name: str
    backend_type: str
    version: str | None
    running: bool


class MarzneshinNodeStatus(str, Enum):
    healthy = "healthy"
    unhealthy = "unhealthy"
    disabled = "disabled"


class MarzneshinNodeConnectionBackend(str, Enum):
    grpcio = "grpcio"
    grpclib = "grpclib"


class MarzneshinNodeSettings(BaseModel):
    min_node_version: str = "v0.2.0"
    certificate: str


class MarzneshinNode(BaseModel):
    id: int | None = Field(None)
    name: str
    address: str
    port: int = 53042
    connection_backend: MarzneshinNodeConnectionBackend = Field(
        default=MarzneshinNodeConnectionBackend.grpclib
    )
    usage_coefficient: float = Field(ge=0, default=1.0)


class MarzneshinNodeResponse(MarzneshinNode):
    xray_version: str | None = None
    status: MarzneshinNodeStatus
    message: str | None = None
    inbound_ids: list[int] | None = None
    backends: list[MarzneshinBackend]

    @property
    def is_have_error(self) -> bool:
        return self.status == MarzneshinNodeStatus.unhealthy

    @property
    def remark(self) -> bool:
        return self.name
