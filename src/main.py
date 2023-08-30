from typing import Annotated

from fastapi import FastAPI, Query

from api import settings, databases, models

app = FastAPI()


@app.post("/items/")
async def add_item(item: models.Item):
    return await databases.add_item(item)


@app.get("/items/")
async def get_items(
    limit: Annotated[int, Query(gt=0, lt=20)] = 2,
    offset: int = 0,
):
    return await databases.get_items(limit, offset)


@app.get("/items/{item_id}/")
async def get_item(item_id: int):
    return await databases.get_item(item_id)


@app.put("/items/{item_id}/")
async def modify_item(item_id: int, modified_item: models.ModifiedItem):
    return await databases.modify_item(item_id, modified_item)


@app.patch("/items/{item_id}/")
async def modify_item_partially(item_id: int, partially_modified_item: models.PartiallyModifiedItem):
    return await databases.modify_item_partially(item_id, partially_modified_item)
