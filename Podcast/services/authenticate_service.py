# In the name of GOD
import httpx
import json
from fastapi import Body


from config import settings
from utils.secure_communicate import Encryption

class AuthenticateService:
    code_keys = {"auth_pod_key1":settings.AUTH_POD_KEY1}
    Encrypt_tools = Encryption(settings.POD_AUTH_SHARED_KEY, code_keys)

    @classmethod
    async def get_authorization(cls, data):
        url = settings.AUTHENTICATION_SERVICE_URL + '/users/authorize_token'
        response = await cls.encrypt_and_send(data, url)
        return response   

    @classmethod
    async def encrypt_and_send(cls, data, url, headers={}):
        encrypted_data = cls.Encrypt_tools.encrypt_data(data)
        async with httpx.AsyncClient() as client:
            headers.update({"internal-service":"podcast"})
            response = await client.post(url=url, data=json.dumps(encrypted_data), headers=headers)
            # print(f"url: {url}\nheaders: {headers}\nencrypted_data:\n\n{json.dumps(encrypted_data)}\nreponse :\n {response.__dict__}")
        if response.status_code >= 500:
            return response
        response._content = json.loads(cls.Encrypt_tools.decrypt_data(response.content))
        return response       

