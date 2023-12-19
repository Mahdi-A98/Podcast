# In the name of GOD
import httpx
import json
from fastapi import Body


from config import settings
from utils.secure_communicate import Encryption

class NotificationService:
    code_keys = {"ntf_pod_key1":settings.NTF_POD_KEY1}
    Encrypt_tools = Encryption(settings.NTF_POD_SHARED_KEY, code_keys)

    @classmethod
    async def send_email_notification(cls, data):
        url = settings.NOTIFICATION_SERVICE_URL + '/notification/send_email_notification'
        response = await cls.encrypt_and_send(data, url)
        return response   

    @classmethod
    async def encrypt_and_send(cls, data, url, headers={}):
        encrypted_data = cls.Encrypt_tools.encrypt_data(data)
        async with httpx.AsyncClient() as client:
            headers.update({"internal-service":"podcast"})
            response = await client.post(url=url, data=json.dumps(encrypted_data), headers=headers)
        if response.status_code >= 500:
            return response
        response._content = json.loads(cls.Encrypt_tools.decrypt_data(response.content))
        return response       