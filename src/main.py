from typing import Annotated, Optional

from aiocouch import CouchDB
from aiocouch import exception as aiocouch_exceptions
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from api import settings

app = FastAPI()


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



@app.post("/items/")
async def add_item(item: Item):
    async with CouchDB(
        settings.COUCHDB_URL, user=settings.COUCHDB_USER, password=settings.COUCHDB_PASSWORD
    ) as couchdb:
        db = await couchdb[settings.COUCHDB_DATABASE]
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
        db = await couchdb[settings.COUCHDB_DATABASE]
        response = []
        async for document in db.docs(limit=limit, skip=offset):
            response.append(document)
        return response


@app.get("/items/{item_id}/")
async def get_item(item_id: int):
    async with CouchDB(
        settings.COUCHDB_URL, user=settings.COUCHDB_USER, password=settings.COUCHDB_PASSWORD
    ) as couchdb:
        db = await couchdb[settings.COUCHDB_DATABASE]
        try:
            doc = await db[f"items:{item_id}"]
        except aiocouch_exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="item_not_found")
        return doc


@app.put("/items/{item_id}/")
async def modify_item(item_id: int, modified_item: ModifiedItem):
    async with CouchDB(
        settings.COUCHDB_URL, user=settings.COUCHDB_USER, password=settings.COUCHDB_PASSWORD
    ) as couchdb:
        db = await couchdb[settings.COUCHDB_DATABASE]
        try:
            doc = await db[f"items:{item_id}"]
        except aiocouch_exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="item_not_found")

        doc.update(modified_item)
        await doc.save()
        return doc


@app.patch("/items/{item_id}/")
async def modify_item_partially(item_id: int, partially_modified_item: PartiallyModifiedItem):
    async with CouchDB(
        settings.COUCHDB_URL, user=settings.COUCHDB_USER, password=settings.COUCHDB_PASSWORD
    ) as couchdb:
        db = await couchdb[settings.COUCHDB_DATABASE]
        try:
            doc = await db[f"items:{item_id}"]
        except aiocouch_exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="item_not_found")

        updated_data = partially_modified_item.dict(exclude_unset=True)
        doc.update(updated_data)
        await doc.save()
        return doc
