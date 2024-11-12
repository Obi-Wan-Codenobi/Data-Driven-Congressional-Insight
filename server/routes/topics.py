from fastapi import APIRouter, Request
from services.topics import get_all_topics
topics_router = APIRouter()


@topics_router.get("/all")
async def response(request: Request):
    return await get_all_topics()
 
