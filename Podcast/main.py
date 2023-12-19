@asynccontextmanager
async def lifespan(app: FastAPI):
    podcast_db = await sess_db()
    collections["podcast_collection"] = podcast_db.database["podcast_collection"]
    collections["episode_collection"] = podcast_db.database["episode_collection"]
    collections["comment_collection"] = podcast_db.database["comment_collection"]
    collections["bookmark_collection"] = podcast_db.database["bookmark_collection"]
    collections["like_collection"] = podcast_db.database["like_collection"]
    yield
    collections.clear()
    podcast_db.client.close()
