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


