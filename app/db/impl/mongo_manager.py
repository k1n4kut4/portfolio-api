import logging
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
# from decouple import config

from app.db.interfaces.database_manager import DatabaseManager
from app.models.blog import Blog_Post_Data
from app.utils.common_helper import validate_data_retrieved, format_data_to_list

class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str, database: str):
        self.client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10
        )
        try:
            await self.client.admin.command('ping') 
            logging.info("Connection successful.")
        except Exception as e:
            logging.info(f"Log in unsuccessful: {e}")
        self.database = self.client[database]

    async def close_database_connection(self):
        self.client.close()

    async def get_posts(self) -> List[Blog_Post_Data]:
        posts_data = self.database.posts.find()
        data_list = []   
        if validate_data_retrieved(posts_data):
            data_list = await format_data_to_list(posts_data) 
            return data_list