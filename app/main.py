from typing import Annotated

from aiocouch import CouchDB
from aiocouch import exception as aiocouch_exceptions
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

import settings

app = FastAPI()


class ModifiedItem(BaseModel):
    name: str
    description: str | None = None
    price: float


class Item(ModifiedItem):
    id: int


@app.post("/items/")
async def add_item(item: Item):
    async with CouchDB(
        settings.COUCHDB_URL, user=settings.COUCHDB_USER, password=settings.COUCHDB_PASSWORD
    ) as couchdb:
        db = await couchdb["stores"]
        item_id = item.id
        item_json = item.dict()
        del item_json["id"]
        try:
            new_doc = await db.create(
                f"items:{item.id}", data=item_json
            )
        except aiocouch_exceptions.ConflictError as e:
            raise HTTPException(status_code=400, detail="item_already_exists")

        await new_doc.save()
        return item


@app.get("/items/")
async def get_items(
    limit: Annotated[int, Query(gt=0, lt=20)] = 2,
    offset: int = 0,
):
    async with CouchDB(
        settings.COUCHDB_URL, user=settings.COUCHDB_USER, password=settings.COUCHDB_PASSWORD
    ) as couchdb:
        db = await couchdb["stores"]
        response = []
        async for document in db.docs(limit=limit, skip=offset):
            response.append(document)
        return response


@app.get("/items/{item_id}/")
async def get_item(item_id: int):
    async with CouchDB(
        settings.COUCHDB_URL, user=settings.COUCHDB_USER, password=settings.COUCHDB_PASSWORD
    ) as couchdb:
        db = await couchdb["stores"]
        doc = await db[f"items:{item_id}"]
        return doc


@app.put("/items/{item_id}/")
async def modify_item(item_id: int, modified_item: ModifiedItem):
    async with CouchDB(
        settings.COUCHDB_URL, user=settings.COUCHDB_USER, password=settings.COUCHDB_PASSWORD
    ) as couchdb:
        db = await couchdb["stores"]
        try:
            doc = await db[f"items:{item_id}"]
        except aiocouch_exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="item_not_found")

        doc.update(modified_item)
        # actually perform the request to save the modification to the server
        await doc.save()
        return doc
