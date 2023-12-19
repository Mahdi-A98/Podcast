# In the name of GOD
import httpx
import json
from fastapi import Body


from config import settings
from utils.secure_communicate import Encryption

class DjangoPodcastService:

    @classmethod
    async def get_podcast_list(cls, data=None, params=None):
        url = settings.DJANGO_PODCAST_SERVICE_URL + '/podcast/podcasts/'
        response = await cls.get(url=url, params=params)
        return response   

    @classmethod
    async def get_podcast_episode_list(cls, podcast_id:int , data=None, params=None):
        assert isinstance(podcast_id, int), "Podcast id should be integer"
        url = settings.DJANGO_PODCAST_SERVICE_URL + f'/podcast/episodes/{podcast_id}/'
        response = await cls.get(url=url, params=params)
        return response   

    @classmethod
    async def get(cls, url, headers={}, params=None):
        async with httpx.AsyncClient() as client:
            headers.update({"internal-service":"podcast"})
            response = await client.get(url=url, headers=headers, params=params)
        return response       


    @classmethod
    async def send(cls, data, url, headers={}, params=None):
        async with httpx.AsyncClient() as client:
            headers.update({"internal-service":"podcast"})
            response = await client.post(url=url, data=data, headers=headers, params=params)
            # print(f"url: {url}\nheaders: {headers}\nencrypted_data:\n\n{json.dumps(encrypted_data)}\nreponse :\n {response.__dict__}")
        if response.status_code >= 500:
            return response
        return response       
