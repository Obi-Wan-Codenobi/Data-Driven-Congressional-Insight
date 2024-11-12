__all__ = ["router"]

from sys import prefix
from fastapi import APIRouter
from .topics import topics_router
from .query import query_router
from .politicians import politician_router

router = APIRouter()
router.include_router(topics_router, prefix="/api/topics")
router.include_router(query_router, prefix="/api/search")
router.include_router(politician_router, prefix="/api/politician")
