# In the name of GOD

from pydantic import BaseModel, Field
from typing import Annotated, Optional, Literal , Union
from uuid import uuid4
from datetime import datetime

def gen_id():
    res_id = uuid4()
    return str(res_id)

class DatedModel(BaseModel):
    created_at: str | datetime = Field(default_factory=datetime.now)
    updated_at: str | datetime = None

class PodcastRelatedType(BaseModel):
    object_type : Literal['episode', 'podcast']
    object_id : int

class BaseComment(PodcastRelatedType):
    text : Optional[str] = None

class Comment(DatedModel, BaseComment):
    id : str = Field(default_factory=gen_id)
    # object_type : Literal['episode', 'podcast']
    # object_id : int
    username : str

class Like(DatedModel, PodcastRelatedType):
    id : str = Field(default_factory=gen_id)
    # object_type : Literal['episode', 'podcast']
    # object_id : int
    username : str

class BookMark(DatedModel, PodcastRelatedType):
    id : str = Field(default_factory=gen_id)
    # object_type : Literal['episode', 'podcast']
    # object_id : int
    username : str

#*************************************************************************************************
#*************************************************************************************************


class PodcastComment(DatedModel):
    id : str = Field(default_factory=gen_id)
    username: str
    podcast_id: str
    text : str = None


class PodcastLike(DatedModel):
    id : str = Field(default_factory=gen_id)
    username: str
    podcast_id: int


class EpisodeComment(DatedModel):
    id : str = Field(default_factory=gen_id)
    username: str
    episode_id: str
    text : str = None


class EpisodeLike(DatedModel):
    id : str = Field(default_factory=gen_id)
    username: str
    episode_id: str


class PodcastBookMark(DatedModel):
    id : str = Field(default_factory=gen_id)
    username: str
    podcast_id: str


class EpisodeBookMark(DatedModel):
    id : str = Field(default_factory=gen_id)
    username: str
    podcast_id: str