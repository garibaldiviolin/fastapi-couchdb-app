from typing import Optional

from pydantic import BaseModel, Field, computed_field


class ModifiedItem(BaseModel):
    name: str
    description: str | None = None
    price: float


class Item(ModifiedItem):
    id: int


class ResponseItem(ModifiedItem):
    temp_id: str = Field(..., validation_alias="_id", exclude=True)

    @computed_field
    @property
    def id(self) -> int:
        return int(self.temp_id[6:])


class PartiallyModifiedItem(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
