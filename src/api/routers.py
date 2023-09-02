from typing import Annotated

from fastapi import APIRouter, Query

from api import databases, models

router = APIRouter()


@router.post("/items/", status_code=201, response_model=models.ResponseItem)
async def add_item(item: models.Item):
    return await databases.add_item(item)


@router.get("/items/", response_model=list[models.ResponseItem])
async def get_items(
    limit: Annotated[int, Query(gt=0, lt=20)] = 2,
    offset: int = 0,
):
    return await databases.get_items(limit, offset)


@router.get("/items/{item_id}/", response_model=models.ResponseItem)
async def get_item(item_id: int):
    return await databases.get_item(item_id)


@router.put("/items/{item_id}/", response_model=models.ResponseItem)
async def modify_item(item_id: int, modified_item: models.ModifiedItem):
    return await databases.modify_item(item_id, modified_item)


@router.patch("/items/{item_id}/", response_model=models.ResponseItem)
async def modify_item_partially(
    item_id: int, partially_modified_item: models.PartiallyModifiedItem
):
    return await databases.modify_item_partially(item_id, partially_modified_item)
