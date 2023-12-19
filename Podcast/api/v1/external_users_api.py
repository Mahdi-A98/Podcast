# In the name of GOD

from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import Response, JSONResponse, HTMLResponse

from pymongo.errors import BulkWriteError, DuplicateKeyError
from pydantic import ValidationError

from typing import Annotated, Mapping, Literal
import json

from models.podcast import (Episode, Podcast, PodcastCollection, EpisodeCollection,
                            PaginatedPodcastCollection, PaginatedEpisodeCollection)

from models.interactions import Like, BookMark, Comment, BaseComment, PodcastRelatedType
from db.pipelines import RETRIVE_COMMENTS_PIPELINE

from config.dependencies import check_login_status, AllowedServices
from db.db import databases, collections
from services.django_podcast import DjangoPodcastService


LoginDep = Annotated[str, Depends(check_login_status)]


router = APIRouter(
    prefix="/podcast",
    tags=["podcasts"],
    responses={404: {"description":"Not found"}, 307: {"detail":"method not allowed"}},
    )


@router.get("/podcast_list", response_description="Podcast list")
async def podcast_list(limit:int=1, offset:int=1):
    podcast_collection = collections['podcast_collection']
    django_response = await DjangoPodcastService.get_podcast_list(params={"limit":limit, "offset":offset})
    response_dict = django_response.json()
    podcasts = PodcastCollection(podcasts=response_dict['results'])

    query = {"id": {"$in": list(map(lambda pod_dict: pod_dict["id"], podcasts.dict()['podcasts']))}}
    pipeline = RETRIVE_COMMENTS_PIPELINE
    pipeline.append({"$match": query})
    try:
        result = await podcast_collection.insert_many(podcasts.dict()['podcasts'], ordered=False)
    except BulkWriteError:
        pass
    results =  podcast_collection.aggregate(pipeline)
    response_dict['results'] = await results.to_list(None)
    paginated_podcasts = PaginatedPodcastCollection(**response_dict)
    return JSONResponse(paginated_podcasts.dict(), status_code=status.HTTP_200_OK)



@router.get("/podcast_episode_list/{podcast_id}", response_description="Podcast's episode list")
async def podcast_episode_list(podcast_id:int, limit:int=1, offset:int=1):
    podcast_collection = collections['podcast_collection']
    episode_collection = collections['episode_collection']
    response = await DjangoPodcastService.get_podcast_episode_list(podcast_id)
    response_dict = response.json()
    episode_ids = list(map(lambda item: item['id'], response_dict['results']))
    episode_models = EpisodeCollection(episodes=response_dict['results'])
    for episode in episode_models.episodes:
        episode.episode_podcast = episode.episode_podcast['id']
    try:
        await podcast_collection.insert_one(Podcast(**response_dict['results'][0]['episode_podcast']).dict())
    except (DuplicateKeyError):
        pass
    try:
        res = await episode_collection.insert_many(episode_models.dict()['episodes'], ordered=False)
    except BulkWriteError as e:
        pass
    podcast = await podcast_collection.find_one(filter={"id": podcast_id}, projection={"_id": 0})
    pipeline = RETRIVE_COMMENTS_PIPELINE
    pipeline.append({"$match": {"id": {"$in": episode_ids}}})
    episodes = await episode_collection.aggregate(pipeline).to_list(None)
    # episodes = await episode_collection.find(filter={"id": {"$in": episode_ids}}, projection={"_id": 0}).to_list(None)
    return JSONResponse({"podcast": podcast, "episodes": episodes}, status_code=status.HTTP_200_OK)


@router.put("/like/{object_id}", response_description="Podcast and episode like endpoint")
async def like(user_data: LoginDep, object_id:int, object_type:Literal['episode', 'podcast']): # depend on login
    podcast_or_episode_collection = collections[f'{object_type}_collection']
    like_collection = collections['like_collection']
    try:
        like = Like(**{"username": user_data['data'].get("username"), "object_id": object_id, "object_type": object_type})
        like_result = await like_collection.insert_one(like.dict())
        like_result = await podcast_or_episode_collection.find_one_and_update({"id": object_id}, {"$addToSet": {'likes': like.username}})
    except ValidationError:
        return JSONResponse({"message": "Wrong Like values"}, status_code=status.HTTP_400_BAD_REQUEST)
    except DuplicateKeyError:
        return JSONResponse({"message": f"this {object_type} is Liked before by this user"}, status_code=status.HTTP_400_BAD_REQUEST)
    if not like_result:
        return JSONResponse({"message": f"Wrong {object_type} id"}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message":f"{object_type.capitalize()} {object_id} Liked successfully", object_type: str(like_result)}, status_code=status.HTTP_200_OK)

