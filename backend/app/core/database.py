from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


client = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.mongo_db_name]


async def get_db():
    return database
