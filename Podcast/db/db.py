databases : Dict[str, pymongo.database.Database] = {}
collections : Dict[str, pymongo.collection.Collection] = {}
class MogodbManager:
    HOST=settings.MONGODB_HOST
    PORT=settings.MONGODB_PORT
    DATABASE = settings.MONGODB_DATABASE

    def __init__(self, database:str=""):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{self.HOST}:{self.PORT}/')
        self.database = self.client.get_database(database or self.DATABASE)

    async def create(self, collection_name:str, instance:dict):
        result = await self.database[collection_name].insert_one(instance)
        return str(result.insert_id)

    async def read_all(self, collection_name:str, fields:dict=None, length=None):
        result = await self.database[collection_name].find(fields or {}).to_list(length)
        return result

    async def read(self, collection_name, _id=None, **kwargs):
        kwargs.update(query = {"_id": ObjectId(_id)}) if _id else None
        return await self.database[collection_name].find_one(kwargs)


    async def update(self, collection_name, _id: str, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        result = await self.database[collection_name].update_one(
            {"_id": ObjectId(_id)}, {"$set": data}
        )
        return bool(result.matched_count)

    async def delete(self, collection_name, _id):
        result = self.database[collection_name].delete_one({"_id":ObjectId(_id)})
        return result.deleted_count
async def sess_db():
    podcast_db = MogodbManager("podcast_db")  
    # podcast_db.database['podcast_collection'].drop_indexes()  
    # podcast_db.database['episode_collection'].drop_indexes() 
    # podcast_db.database['like_collection'].drop_indexes() 
    podcast_db.database['podcast_collection'].create_index("id", unique=True) 
    podcast_db.database['comment_collection'].create_index("id", unique=True) 
    podcast_db.database['bookmark_collection'].create_index("id", unique=True)
