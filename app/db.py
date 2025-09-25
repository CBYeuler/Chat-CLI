from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI, DB_NAME

# Initialize MongoDB client and database
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]
users_collection = db["users"]
messages_collection = db["messages"]
rooms_collection = db["rooms"]

