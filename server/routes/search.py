from fastapi import FastAPI, APIRouter, Request
import time
import asyncio
from services.search import search_query

query_router = APIRouter()


@query_router.post('/documents')
async def search_response(request: Request):
    data_json = await request.json()
    return await search_query(data_json)

