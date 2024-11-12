from fastapi import FastAPI, APIRouter, Request
import time
import asyncio
from services.politicians import get_all_politicians

politician_router = APIRouter()


@politician_router.get('/all')
async def search_response():
    return await get_all_politicians()
