import asyncio
import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

load_dotenv()
mongodb_uri = os.getenv("MONGODB_URI")
async def check_connection():
    if not mongodb_uri:
        raise RuntimeError("MONGODB_URI is missing. Add it to backend/.env.")
    client= AsyncMongoClient(mongodb_uri,server_api=ServerApi("1"),serverSelectionTimeoutMS=5000,)
    try:
        await client.admin.command({"ping": 1})
        print("Successfully connected to MongoDB Atlas.")
    except Exception as error:
        print(f"MongoDB connection failed: {error}")
        raise
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(check_connection())