from fastapi import FastAPI, APIRouter, Request
import time
import asyncio
from services.search import topic_query

query_router = APIRouter()


@query_router.post('/topic')
async def search_response(request: Request):
    data_json = await request.json()
    return await topic_query(data_json)

