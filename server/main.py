from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from caching import CacheMiddleware
import os
import ollama
from database import conn, create_table
from routes import app as routes_app
from logging_config import logger
from player_utils import fetch_external_players
from database_operations import store_players

# Configure Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
ollama.host = OLLAMA_HOST

# Pull the model on startup
try:
    logger.info(f"Pulling llama3.2:1b model from host: {OLLAMA_HOST}")
    ollama.pull("llama3.2:1b")
    logger.info("Successfully pulled llama3.2:1b model")
except Exception as e:
    logger.error(f"Failed to pull llama3.2:1b model: {e}")
    # Add more detailed error logging
    logger.exception("Detailed error pulling Ollama model")

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

@app.on_event("startup")
async def populate_players():
    """
    Fetch players from external API and populate the database on startup.
    """
    if conn:
        try:
            players = await fetch_external_players()
            if players:
                store_players(conn, players)
                logger.info(f"Successfully populated database with {len(players)} players")
            else:
                logger.warning("No players fetched from external API")
        except Exception as e:
            logger.error(f"Error populating players: {e}")
