# In the name of GOD

import jwt
import base64
import random
import json
import uuid
from datetime import datetime, timedelta


class Encryption:

    def __init__(self, service_shared_key:str, code_keys:dict=None):
        self.service_shared_key = service_shared_key
        self.code_keys = code_keys or {}
        
    def decrypt_data(self, data):
        payload = jwt.decode(data, self.service_shared_key, algorithms=['HS256'])
        if payload:
            decoded_data = self.decode_payload(payload)
            return decoded_data
        return None

    def encrypt_data(self, data, jti=None, exp=10):
        data = json.dumps(data)
        key_name = list(self.code_keys.keys())[random.randint(0, len(self.code_keys.keys())-1)]
        payload = {
            "data": self.Encode(self.code_keys[key_name], data),
            "key_name": key_name,
            'exp': int((datetime.now() + timedelta(seconds=exp+100)).timestamp()),
            'iat': datetime.now().timestamp(),
            'jti': jti or uuid.uuid4().hex
        }
        token = jwt.encode(payload, self.service_shared_key, algorithm='HS256')
        return token

    def decode_payload(self, payload):
        key = self.code_keys[payload.get('key_name')]
        return self.Decode(key, payload.get("data"))

    @staticmethod
    def Encode(key:str, message:str):
        assert isinstance(message, str), "message should be string  "           
        enc=[]
        for i in range(len(message)):
                key_c = key[i % len(key)]
                enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
        return base64.urlsafe_b64encode("".join(enc).encode(errors="ignore")).decode(errors="ignore") 
    
    @staticmethod
    def Decode(key, message): 
        dec = []              
        message = base64.urlsafe_b64decode(message).decode(errors="ignore")
        for i in range(len(message)):     
                key_c = key[i % len(key)] 
                dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256)) 
        return "".join(dec)