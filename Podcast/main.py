# In the name of GOD

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager


from api.v1 import external_users_api
from db.db import collections, databases, sess_db
from config.middlewares import InternalSecurityMiddleware



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

app = FastAPI(lifespan=lifespan)
app.include_router(external_users_api.router)
app.add_middleware(InternalSecurityMiddleware)


@app.get("/")
def root():
    return JSONResponse({"message": "Hello...this is podcast service"}, status_code=200)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8006, log_level="info", reload=True)
    # uvicorn.run(app, host="localhost", port=8006, log_level="debug")