from fastapi import APIRouter, Request
from services.home_data import get_home_data
home_router = APIRouter()


@home_router.get("/")
async def response(request: Request):
    return await get_home_data()
 
