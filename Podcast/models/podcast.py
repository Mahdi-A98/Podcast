# In the name of GOD


from pydantic import ConfigDict, BaseModel, Field, EmailStr, StringConstraints
from typing import Optional, List, Required, Annotated, List, Union
from bson import ObjectId
from datetime import datetime

from .interactions import EpisodeBookMark, EpisodeComment, EpisodeLike , Like, Comment, BookMark
from .interactions import PodcastBookMark, PodcastComment, PodcastLike


class DatedModel(BaseModel):
    created_at: str | datetime
    updated_at: str |datetime

class PodcastImage(DatedModel):
    id: int
    url: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None

class PodcastAuthor(DatedModel):
    id: int
    name : str


class PodcastUrl(DatedModel):
    id: int
    url: Optional[str] = None
    title: Optional[str] = None
    is_saved: Optional[bool] = None

class Category(BaseModel):
    name : Optional[str] = None

class Podcast(BaseModel):
    id: int
    podcast_image: PodcastImage
    podcast_author: PodcastAuthor
    category: Optional[Category] = None
    podcast_url: Optional[PodcastUrl] = None
    title: str
    language: str = "en"
    itunes_type: str
    copy_right: str
    itunes_explicit: Optional[str | bool]
    description: str
    pubDate: Optional[str] = None
    lastBuildDate: Optional[str] = None
    link: Optional[str] = None
    itunes_subtitle: Optional[str] = None
    itunes_keywords: Optional[str] = None
    itunes_image: Optional[str] = None
    podcast_generator: Optional[int] = None
    podcast_owner: Optional[int] = None
    # likes : Optional[List[PodcastLike]] = []
    # comments : Optional[List[PodcastComment]] = []
    # bookmarks : Optional[List[PodcastBookMark]] = []
    likes : List = []
    comments : List = []
    bookmarks : List = [] 

class Episode(BaseModel):
    id : int
    episode_podcast : Optional[int | dict]
    title : str = None
    guid : Optional[str] = None
    itunes_duration : Optional[str |datetime] = None
    itunes_episodeType : Optional[str] = None
    itunes_explicit : Optional[str | bool] = None
    description : Optional[str] = None
    enclosure : Optional[str] = None
    link : Optional[str] = None
    pubDate : Optional[str | datetime] = None
    itunes_keywords : Optional[str] = None
    itunes_player : Optional[str] = None
    episode_author : Optional[int] = None
    # likes : Optional[List[EpisodeLike]] = []
    # comments : Optional[List[EpisodeComment]] = []
    # bookmarks : Optional[List[EpisodeBookMark]] = []
    likes : List = []
    comments : List = []
    bookmarks : List = [] 

    
class EpisodeCollection(BaseModel):
    """
    A container holding a list of `Episode Model` instances.
    """

    episodes: List[Episode]

class PodcastCollection(BaseModel):
    """
    A container holding a list of `Podcast Model` instances.
    """

    podcasts: List[Podcast]


class PaginatedPodcastCollection(BaseModel):
    """
    A container holding a list of `Podcast Model` instances.
    """
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: Optional[List[Podcast]] = []


class PaginatedEpisodeCollection(BaseModel):
    """
    A container holding a list of `Podcast Model` instances.
    """
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: Optional[List[Episode]] = []
