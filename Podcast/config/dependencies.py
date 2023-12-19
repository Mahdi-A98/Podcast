# In the name of GOD
from fastapi import Header, HTTPException, Request
from typing import Annotated, List

from services import SERVICE_CLASSES


async def check_login_status(request: Request):
    data = {"access_token":request.headers.get("access-token"), "refresh_token":request.headers.get("refresh-token")}
    auth_response = await SERVICE_CLASSES['authentication'].get_authorization(data)
    if auth_response.status_code != 200:
        raise HTTPException(detail=auth_response.json(), status_code=auth_response.status_code)
    print(f"check_login_status auth_response.json(): {auth_response.json()}")
    return auth_response.json()



async def get_service(request: Request):
    if not request.headers.get("internal-service"):
        raise HTTPException(detail="Access denied.", status_code=403)
    return True


class AllowedServices:
    def __init__(self, allowed_services:List):
        self.allowed_services = allowed_services

    async def __call__(self, request:Request):
        if not request.headers.get("internal-service"):
            raise HTTPException(detail="Access denied.", status_code=403)
        if not request.headers.get("internal-service") in self.allowed_services:
            raise HTTPException(detail=f"This endpoint is restricted to {' ,'.join(self.allowed_services)} services.", status_code=403)
        return True