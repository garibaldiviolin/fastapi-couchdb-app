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


async def create_item():
    async with aiocouch.CouchDB(
        settings.COUCHDB_URL,
        user=settings.COUCHDB_USER,
        password=settings.COUCHDB_PASSWORD,
    ) as couchdb:
        db = await couchdb[COUCHDB_TEST_DATABASE]
        item = {
            "name": "soap3",
            "description": "This is a soap",
            "price": 1.54,
        }
        new_doc = await db.create(databases.format_item_id(81238), data=item)
        await new_doc.save()
        return item


@pytest.fixture
def existing_item(database):
    return asyncio.run(create_item())
