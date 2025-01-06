from pydantic import BaseModel


class MarzneshinServiceResponce(BaseModel):
    id: int
    name: str | None
    inbound_ids: list[int]
    user_ids: list[int]

    @property
    def remark(self):
        return f"{self.name} [{len(self.user_ids)}]"

    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        base_dict["remark"] = self.remark
        return base_dict
