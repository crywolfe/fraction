from fastapi import FastAPI, HTTPException, Query, Body
from typing import Dict, Any
import json

from logging_config import logger
from database import conn
from database_operations import (
    get_player_by_id,
    store_players,
    fetch_paginated_players,
    update_player,
)
from player_utils import fetch_external_players
from ollama_service import generate_player_description

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World from Backend"}


...


@app.get("/players")
async def get_players(
    page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)
) -> Dict[str, Any]:
    logger.info(f"Received request for players - Page: {page}, Page Size: {page_size}")

    try:
        # Check if database is empty
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM players")
        player_count = cursor.fetchone()[0]
        cursor.close()

        # If no players exist, fetch and populate
        if player_count == 0:
            logger.info("No players in database. Fetching and populating...")

            # Fetch players from external API
            external_players = await fetch_external_players()

            # Standardize keys to snake_case
            standardized_players = [
                {k.lower().replace(" ", "_"): v for k, v in player.items()}
                for player in external_players
            ]

            # Store players in the database using standardized data
            if not store_players(conn, standardized_players):
                raise HTTPException(status_code=500, detail="Failed to store players")

        # Fetch paginated players from the database
        result = fetch_paginated_players(conn, page, page_size)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to fetch players")

        return result
    except Exception as e:
        logger.error(f"Error in get_players: {e}")
        raise HTTPException(status_code=500, detail=str(e))


...


@app.put("/players/{player_id}")
async def update_player_route(player_id: int, player: Dict[str, Any] = Body(...)):
    logger.info(
        f"Received update request for player ID: {player_id} with data: {player}"
    )

    try:
        if update_player(conn, player_id, player):
            logger.info(f"Player ID {player_id} updated successfully")
            return {"message": f"Player ID {player_id} updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Player not found")
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/player/{player_id}/description")
async def generate_player_description_route(player_id: int):
    """
    Generate a concise player description using Ollama.
    """
    logger.info(f"Generating description for player ID: {player_id}")

    # Fetch player record
    player_record = get_player_by_id(conn, player_id)
    if not player_record:
        logger.warning(f"Player not found with ID: {player_id}")
        raise HTTPException(status_code=404, detail="Player not found")

    player_name = player_record[2]["player_name"]
    position = player_record[2]["position"]
    data = player_record[2]
    logger.info(f"Fetched player: {player_name}, position: {position}, {player_record}")
    # Parse player data
    if isinstance(data, str):
        player_data = json.loads(data)
    else:
        player_data = data

    # Generate description
    description = generate_player_description(
        player_name, position, player_data.get("team"), player_data
    )

    # Update player data with description
    player_data["description"] = description

    # Update player in database
    if update_player(conn, player_id, player_data):
        return {"description": description}
    else:
        logger.error(f"Failed to update player {player_id} with description")
        raise HTTPException(
            status_code=500, detail="Failed to update player description"
        )
