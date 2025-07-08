from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["AuthPilot"]
client_collections = db["client_list"]