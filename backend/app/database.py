from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from app.config import Settings

def create_mongodb_client(settings):
    return AsyncMongoClient(settings.mongodb_uri,server_api=ServerApi("1"),serverSelectionTimeoutMS=5000,)

async def verify_mongodb_connection(client,):
    await client.admin.command({"ping": 1})