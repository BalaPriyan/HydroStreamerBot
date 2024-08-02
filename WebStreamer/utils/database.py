# Code optimized by fyaz05
# Code from SpringsFern

import pymongo
import time
import motor.motor_asyncio
from bson.objectid import ObjectId
from bson.errors import InvalidId
from WebStreamer.server.exceptions import FIleNotFound
from WebStreamer.vars import Var

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.black = self.db.blacklist
        self.file = self.db.file
   
    def new_user(self, id):
        return dict(
            id=id,
            join_date=time.time(),
            agreed_to_tos=False,
            Plan="Free"
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def get_user(self, id):
        return await self.col.find_one({'id': int(id)})

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def agreed_tos(self, user_id):
        update_data = {
            "agreed_to_tos": True,
            "when_agreed_to_tos": time.time(),
        }
        await self.col.update_one({"id": int(user_id)}, {"$set": update_data})

    def black_user(self, id):
        return dict(
            id=id,
            ban_date=time.time(),
        )

    async def ban_user(self, id):
        user = self.black_user(id)
        await self.black.insert_one(user)
        await self.delete_user(id)

    async def unban_user(self, id):
        await self.black.delete_one({'id': int(id)})

    async def is_user_banned(self, id):
        return await self.black.find_one({'id': int(id)}) is not None

    async def total_banned_users_count(self):
        return await self.black.count_documents({})

    async def add_file(self, file_info):
        file_info["time"] = time.time()
        existing_file = await self.get_file_by_fileuniqueid(file_info["user_id"], file_info["file_unique_id"])
        
        if existing_file:
            return existing_file["_id"]
        
        result = await self.file.insert_one(file_info)
        return result.inserted_id

    async def find_files(self, user_id, range):
        cursor = self.file.find({"user_id": user_id}).skip(range[0] - 1).limit(range[1] - range[0] + 1).sort('_id', pymongo.DESCENDING)
        total_files = await self.file.count_documents({"user_id": user_id})
        return cursor, total_files

    async def get_file(self, _id):
        try:
            file_info = await self.file.find_one({"_id": ObjectId(_id)})
            if not file_info:
                raise FIleNotFound
            return file_info
        except InvalidId:
            raise FIleNotFound

    async def get_file_by_fileuniqueid(self, id, file_unique_id, many=False):
        if many:
            return self.file.find({"file_unique_id": file_unique_id})
        
        return await self.file.find_one({"user_id": id, "file_unique_id": file_unique_id})

    async def total_files(self, id=None):
        query = {"user_id": id} if id else {}
        return await self.file.count_documents(query)

    async def delete_one_file(self, _id):
        await self.file.delete_one({'_id': ObjectId(_id)})

    async def update_file_ids(self, _id, file_ids: dict):
        await self.file.update_one({"_id": ObjectId(_id)}, {"$set": {"file_ids": file_ids}})

    async def link_available(self, id):
        if not Var.LINK_LIMIT:
            return True

        user = await self.col.find_one({"id": id})
        if user.get("Plan") == "Plus":
            return "Plus"
        
        if user.get("Plan") == "Free":
            files = await self.file.count_documents({"user_id": id})
            return files <= Var.LINK_LIMIT
        return False