from motor import motor_asyncio

from app.config import settings


async def get_db():

    client = motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URI, serverSelectionTimeoutMS=1000)
    return client["mongo_tech"]
