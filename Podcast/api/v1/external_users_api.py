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
