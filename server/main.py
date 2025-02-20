from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from caching import CacheMiddleware
import logging
import os
import ollama
from database import conn, create_table
from routes import app as routes_app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Ollama
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
ollama.host = OLLAMA_HOST

# Pull the model on startup
try:
    logger.info("Pulling Llama3.2 model...")
    ollama.pull('llama3.2')
    logger.info("Successfully pulled Llama3.2 model")
except Exception as e:
    logger.error(f"Failed to pull Llama3.2 model: {e}")

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
