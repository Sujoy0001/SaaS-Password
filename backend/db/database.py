from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["PlugAPI"]
client_collections = db["CLIENTS"]
client_user_collections = db["USERS"]