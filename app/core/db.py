import motor.motor_asyncio

from app.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URI)
db = client.mongo_tech
