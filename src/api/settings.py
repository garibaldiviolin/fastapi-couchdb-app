from decouple import config

COUCHDB_URL = config("COUCHDB_URL")
COUCHDB_USER = config("COUCHDB_USER")
COUCHDB_PASSWORD = config("COUCHDB_PASSWORD")