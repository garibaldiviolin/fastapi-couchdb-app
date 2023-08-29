from typing import Union

from aiocouch import CouchDB
from aiocouch.exception import ConflictError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float


@app.post("/items/")
async def add_item(item: Item):
    async with CouchDB(
        "http://couchserver:5984", user="admin", password="password123"
    ) as couchdb:
        db = await couchdb["stores"]
        item_id = item.id
        item_json = item.dict()
        del item_json["id"]
        try:
            new_doc = await db.create(
                f"items:{item.id}", data=item_json
            )
        except ConflictError as e:
            raise HTTPException(status_code=400, detail="item_already_exists")

        await new_doc.save()
        return item


@app.get("/items/{item_id}/")
async def get_item(item_id: int):
    async with CouchDB(
        "http://couchserver:5984", user="admin", password="password123"
    ) as couchdb:
        db = await couchdb["stores"]
        doc = await db[f"items:{item_id}"]
        return doc
