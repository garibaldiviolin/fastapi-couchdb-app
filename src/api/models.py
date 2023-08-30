from typing import Optional

from pydantic import BaseModel


class ModifiedItem(BaseModel):
    name: str
    description: str | None = None
    price: float


class Item(ModifiedItem):
    id: int


class PartiallyModifiedItem(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
