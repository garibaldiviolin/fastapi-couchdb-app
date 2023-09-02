import asyncio

import aiocouch
import pytest

from api import databases, settings

COUCHDB_TEST_DATABASE = "testing_database"


async def create_database():
    async with aiocouch.CouchDB(
        settings.COUCHDB_URL,
        user=settings.COUCHDB_USER,
        password=settings.COUCHDB_PASSWORD,
    ) as couchdb:
        await couchdb.create(COUCHDB_TEST_DATABASE)


async def delete_database():
    async with aiocouch.CouchDB(
        settings.COUCHDB_URL,
        user=settings.COUCHDB_USER,
        password=settings.COUCHDB_PASSWORD,
    ) as couchdb:
        db = await couchdb[COUCHDB_TEST_DATABASE]
        await db.delete()


@pytest.fixture
def database():
    asyncio.run(create_database())
    yield
    asyncio.run(delete_database())


@pytest.fixture
def item_dict():
    return {
        "name": "soap3",
        "description": "This is a soap",
        "price": 1.54,
    }


async def create_item(item_id, item_dict):
    async with aiocouch.CouchDB(
        settings.COUCHDB_URL,
        user=settings.COUCHDB_USER,
        password=settings.COUCHDB_PASSWORD,
    ) as couchdb:
        db = await couchdb[COUCHDB_TEST_DATABASE]
        item = item_dict.copy()
        new_doc = await db.create(databases.format_item_id(item_id), data=item)
        await new_doc.save()
        return item


@pytest.fixture
def item_id():
    return 81238


@pytest.fixture
def item_id2():
    return 81239


@pytest.fixture
def item(database, item_id, item_dict):
    asyncio.run(create_item(item_id, item_dict))
    return {"id": item_id, **item_dict}


@pytest.fixture
def items(database, item_id, item_id2, item_dict):
    asyncio.run(create_item(item_id, item_dict))
    asyncio.run(create_item(item_id2, item_dict))
    return [{"id": item_id, **item_dict}, {"id": item_id2, **item_dict}]
