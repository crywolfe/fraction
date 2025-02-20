from fastapi import FastAPI, HTTPException, Query, Body
import httpx
import ollama
import random
from typing import List, Dict, Any
import logging
import json
from database import conn

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World from Backend"}

@app.get("/players")
async def get_players(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
) -> Dict[str, Any]:
    logger.info(f"Received request for players - Page: {page}, Page Size: {page_size}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.hirefraction.com/api/test/baseball")
            response.raise_for_status()
            players = response.json()
            
            # Standardize keys to snake_case
            standardized_players = [{k.lower().replace(' ', '_'): v for k, v in player.items()} for player in players]
            
            # Store players in the database
            if conn:
                cursor = conn.cursor()
                try:
                    for player in standardized_players:
                        # Extract name, position, and team
                        name = player.get('name', 'Unknown')
                        position = player.get('position', 'Unknown')
                        
                        # Store the rest of the player data as JSON
                        logger.info(f"Player data before JSON conversion: {player}")
                        data = json.dumps(player)
                        logger.info(f"Type of data before database insertion: {type(data)}")
                        # Insert player data into the database
                        cursor.execute("""
                            INSERT INTO players (player_name, position, data)
                            VALUES (%s, %s, %s)
                        """, (name, position, data))
                    conn.commit()
                    logger.info("Players stored in the database")
                except Exception as e:
                    logger.error(f"Database error: {e}")
                    conn.rollback()  # Rollback in case of error
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                logger.error("No database connection")
                raise HTTPException(status_code=500, detail="Database connection failed")
            
            # Database interaction for pagination
            if conn:
                cursor = conn.cursor()
                try:
                    # Calculate offset
                    offset = (page - 1) * page_size
                    
                    # Fetch players from the database with pagination
                    cursor.execute("""
                        SELECT id, player_name, position, data FROM players
                        LIMIT %s OFFSET %s
                    """, (page_size, offset))
                    
                    player_records = cursor.fetchall()
                    
                    # Convert records to a list of dictionaries
                    players = []
                    for record in player_records:
                        player = {
                            "id": record[0],
                            "player_name": record[1],
                            "position": record[2],
                            **record[3]  # Merge the JSON data into the player dictionary
                        }
                        players.append(player)
                    
                    # Get total number of players
                    cursor.execute("SELECT COUNT(*) FROM players")
                    total_players = cursor.fetchone()[0]
                    total_pages = (total_players + page_size - 1) // page_size
                    
                    logger.info(f"Pagination details - Total Players: {total_players}, Total Pages: {total_pages}")
                    
                    return {
                        "players": players,
                        "total_players": total_players,
                        "total_pages": total_pages,
                        "current_page": page,
                        "page_size": page_size
                    }
                except Exception as e:
                    logger.error(f"Database error: {e}")
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                logger.error("No database connection")
                raise HTTPException(status_code=500, detail="Database connection failed")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error: {e}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            logger.error(f"Request Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.put("/players/{player_id}")
async def update_player(player_id: int, player: Dict[str, Any] = Body(...)):
    logger.info(f"Received update request for player ID: {player_id} with data: {player}")
    
    if conn:
        cursor = conn.cursor()
        try:
            logger.info(f"Player data before JSON conversion: {player}")
            # Convert player data to JSON
            player_data = json.dumps(player)
            
            # Update player data in the database
            cursor.execute("""
                UPDATE players
                SET data = %s
                WHERE id = %s
            """, (player_data, player_id))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Player not found")
            
            conn.commit()
            logger.info(f"Player ID {player_id} updated successfully")
            return {"message": f"Player ID {player_id} updated successfully"}
        except Exception as e:
            logger.error(f"Database error: {e}")
            conn.rollback()  # Rollback in case of error
            raise HTTPException(status_code=500, detail=str(e))
    else:
        logger.error("No database connection")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.get("/player/{player_id}/description")
async def generate_player_description(player_id: int):
    """
    Generate a concise player description using Ollama
    
    Args:
        player_id (int): ID of the player to generate description for
    
    Returns:
        Dict containing the generated description
    """
    logger.info(f"Generating description for player ID: {player_id}")
    
    # First, fetch the players to get player details
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.hirefraction.com/api/test/baseball")
            response.raise_for_status()
            players = response.json()
            
            # Find the specific player
            player = next((p for p in players if p.get('id') == player_id), None)
            
            if not player:
                logger.warning(f"Player not found with ID: {player_id}")
                raise HTTPException(status_code=404, detail="Player not found")
            
            # Prepare prompt for description generation
            prompt = f"""Generate a concise 280-character description for a baseball player with these details:
            Name: {player.get('name', 'Unknown')}
            Position: {player.get('position', 'Unknown')}
            Team: {player.get('team', 'Unknown')}
            
            Include career highlights, playing style, and personal background."""
            
            try:
                # Generate description using Ollama
                response = ollama.chat(
                    model='llama3.2:3b',
                    messages=[{'role': 'user', 'content': prompt}]
                )
                
                # Truncate to 280 characters
                description = response['message']['content'][:280]
                
                logger.info(f"Description generated for player {player_id}")
                return {"description": description}
            
            except Exception as e:
                # Fallback description if generation fails
                logger.error(f"Description generation failed: {e}")
                fallback_descriptions = [
                    f"A talented {player.get('position', 'player')} with a passion for the game.",
                    f"Bringing skill and determination to {player.get('team', 'the team')}.",
                    "A rising star in baseball, known for precision and teamwork."
                ]
                return {"description": random.choice(fallback_descriptions)}
        
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error: {e}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            logger.error(f"Request Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))