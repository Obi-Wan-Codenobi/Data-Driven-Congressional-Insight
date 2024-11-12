from typing import Annotated
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import router
import os
import sys
import dotenv

dotenv.load_dotenv()
STATIC_IMAGE_PATH= os.getenv("STATIC_IMAGE_PATH")
STATIC_WEB_PATH= os.getenv("STATIC_WEB_PATH")

app = FastAPI()
app.include_router(router)


'''
Enable CORSMiddleware

Note: This will need to be changed in the future.
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Headers", "Content-Type", "Authorization", "Access-Control-Allow-Origin", "Set-Cookie", "Access-Control-Allow-Credentials"],
)

app.mount("/" + STATIC_IMAGE_PATH, StaticFiles(directory=STATIC_IMAGE_PATH), name=STATIC_IMAGE_PATH)
app.mount("/", StaticFiles(directory=STATIC_WEB_PATH, html = True), name="WEBSITE")
