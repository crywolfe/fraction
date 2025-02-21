import psycopg2
from psycopg2 import sql
import json
from logging_config import logger
from typing import Dict, Any, Optional, Tuple

def get_player_by_id(conn, player_id) -> Optional[Tuple]:
    """
    Fetch a player by their ID from the database.
    
    Args:
        conn: Database connection
        player_id: ID of the player to fetch
    
    Returns:
        Tuple containing player details or None if not found
    """
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                sql.SQL(
                    "SELECT player_name, position, data FROM players WHERE id = %s"
                ),
                (player_id,),
            )
            return cursor.fetchone()
        except psycopg2.Error as e:
            logger.error(f"Error fetching player: {e}")
            return None
        finally:
            cursor.close()
    else:
        return None

def store_players(conn, standardized_players: list) -> bool:
    """
    Store players in the database.
    
    Args:
        conn: Database connection
        standardized_players: List of player dictionaries
    
    Returns:
        Boolean indicating success or failure
    """
    if not conn:
        logger.error("No database connection")
        return False

    cursor = conn.cursor()
    try:
        for player in standardized_players:
            name = player.get("name", "Unknown")
            position = player.get("position", "Unknown")
            logger.info(f"Player data before JSON conversion: {player}")
            data = json.dumps(player)
            cursor.execute(
                """
                INSERT INTO players (player_name, position, data)
                VALUES (%s, %s, %s)
                """,
                (name, position, data),
            )
        conn.commit()
        logger.info("Players stored in the database")
        return True
    except Exception as e:
        logger.error(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def fetch_paginated_players(conn, page: int, page_size: int) -> Dict[str, Any]:
    """
    Fetch paginated players from the database.
    
    Args:
        conn: Database connection
        page: Current page number
        page_size: Number of players per page
    
    Returns:
        Dictionary with players and pagination details
    """
    if not conn:
        logger.error("No database connection")
        return {}

    cursor = conn.cursor()
    try:
        offset = (page - 1) * page_size
        cursor.execute(
            """
            SELECT id, player_name, position, data FROM players
            LIMIT %s OFFSET %s
            """,
            (page_size, offset),
        )
        player_records = cursor.fetchall()
        players_list = []
        for record in player_records:
            data_field = record[3]
            # Check if data_field is already a dict
            if isinstance(data_field, str):
                player_data = json.loads(data_field)
            else:
                player_data = data_field
            player = {
                "id": record[0],
                "player_name": record[1],
                "position": record[2],
                **player_data,
            }
            players_list.append(player)
        
        cursor.execute("SELECT COUNT(*) FROM players")
        total_players = cursor.fetchone()[0]
        total_pages = (total_players + page_size - 1) // page_size
        
        logger.info(
            f"Pagination details - Total Players: {total_players}, Total Pages: {total_pages}"
        )
        
        return {
            "players": players_list,
            "total_players": total_players,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
        }
    except Exception as e:
        logger.error(f"Database error: {e}")
        return {}
    finally:
        cursor.close()

def update_player(conn, player_id: int, player_data: Dict[str, Any]) -> bool:
    """
    Update a player's data in the database.
    
    Args:
        conn: Database connection
        player_id: ID of the player to update
        player_data: Updated player data
    
    Returns:
        Boolean indicating success or failure
    """
    if not conn:
        logger.error("No database connection")
        return False

    cursor = conn.cursor()
    try:
        player_json = json.dumps(player_data)
        cursor.execute(
            """
            UPDATE players
            SET data = %s
            WHERE id = %s
            """,
            (player_json, player_id),
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()