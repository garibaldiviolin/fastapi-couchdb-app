from aiocouch import CouchDB
from aiocouch import exception as aiocouch_exceptions
from fastapi import HTTPException

from api import models, settings


def format_item_id(item_id: int):
    return f"items:{item_id}"


async def add_item(item: models.Item):
    async with CouchDB(
        settings.COUCHDB_URL,
        user=settings.COUCHDB_USER,
        password=settings.COUCHDB_PASSWORD,
    ) as couchdb:
        db = await couchdb[settings.COUCHDB_DATABASE]
        item_json = item.model_dump()
        del item_json["id"]
        try:
            new_doc = await db.create(format_item_id(item.id), data=item_json)
        except aiocouch_exceptions.ConflictError:
            raise HTTPException(status_code=400, detail="item_already_exists")

        await new_doc.save()
        return new_doc.data


async def get_items(limit: int, offset: int | None = 0):
    async with CouchDB(
        settings.COUCHDB_URL,
        user=settings.COUCHDB_USER,
        password=settings.COUCHDB_PASSWORD,
    ) as couchdb:
        db = await couchdb[settings.COUCHDB_DATABASE]
        response = []
        async for document in db.docs(limit=limit, skip=offset):
            response.append(document.data)
        return response


async def get_item(item_id: int):
    async with CouchDB(
        settings.COUCHDB_URL,
        user=settings.COUCHDB_USER,
        password=settings.COUCHDB_PASSWORD,
    ) as couchdb:
        db = await couchdb[settings.COUCHDB_DATABASE]
        try:
            doc = await db[format_item_id(item_id)]
        except aiocouch_exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="item_not_found")
        return doc.data


async def modify_item(item_id: int, modified_item: models.ModifiedItem):
    async with CouchDB(
        settings.COUCHDB_URL,
        user=settings.COUCHDB_USER,
        password=settings.COUCHDB_PASSWORD,
    ) as couchdb:
        db = await couchdb[settings.COUCHDB_DATABASE]
        try:
            doc = await db[format_item_id(item_id)]
        except aiocouch_exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="item_not_found")

        doc.update(modified_item)
        await doc.save()
        return doc.data


async def modify_item_partially(
    item_id: int, partially_modified_item: models.PartiallyModifiedItem
):
    async with CouchDB(
        settings.COUCHDB_URL,
        user=settings.COUCHDB_USER,
        password=settings.COUCHDB_PASSWORD,
    ) as couchdb:
        db = await couchdb[settings.COUCHDB_DATABASE]
        try:
            doc = await db[format_item_id(item_id)]
        except aiocouch_exceptions.NotFoundError:
            raise HTTPException(status_code=404, detail="item_not_found")

        updated_data = partially_modified_item.model_dump(exclude_unset=True)
        doc.update(updated_data)
        await doc.save()
        return doc.data
