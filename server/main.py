from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from caching import CacheMiddleware
import logging
from database import conn, create_table
from routes import app as routes_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# app.add_middleware(CacheMiddleware)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", routes_app)

if conn:
    create_table(conn)
