import psycopg2
from psycopg2 import sql
import json
from logging_config import logger
from typing import Dict, Any, Optional, Tuple, List

def safe_int(value: Any) -> Optional[int]:
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None

def safe_float(value: Any) -> Optional[float]:
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None

def get_player_by_id(conn, player_id) -> Optional[Tuple]:
    """
    Fetch a player by their ID from the database.
    """
    if not conn:
        return None
    with conn.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("SELECT player_name, position, data FROM players WHERE id = %s"),
                (player_id,)
            )
            return cursor.fetchone()
        except psycopg2.Error as e:
            logger.error(f"Error fetching player: {e}")
            return None

def store_players(conn, players: List[Dict[str, Any]]) -> bool:
    """
    Store players in the database with minimal processing.
    """
    if not conn:
        logger.error("No database connection")
        return False

    logger.info(f"Storing {len(players)} players")
    try:
        for player in players:
            # Use 'player_name' key; fallback to 'name'
            player_name = player.get("player_name") or player.get("name") or "Unknown"
            position = player.get("position") or "Unknown"
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO players (
                        player_name, position,
                        games, hits, at_bat, runs,
                        double_2b, third_baseman, home_run,
                        run_batted_in, a_walk, strikeouts,
                        stolen_base, caught_stealing,
                        avg, on_base_percentage,
                        slugging_percentage, on_base_plus_slugging,
                        data
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    RETURNING id
                    """,
                    (
                        player_name,
                        position,
                        safe_int(player.get("games")),
                        safe_int(player.get("hits")),
                        safe_int(player.get("at-bat") or player.get("at_bat")),
                        safe_int(player.get("runs")),
                        safe_int(player.get("double_(2b)")),
                        safe_int(player.get("third_baseman")),
                        safe_int(player.get("home_run")),
                        safe_int(player.get("run_batted_in")),
                        safe_int(player.get("a_walk")),
                        safe_int(player.get("strikeouts")),
                        safe_int(player.get("stolen_base")),
                        safe_int(player.get("caught_stealing")),
                        safe_float(player.get("avg")),
                        safe_float(player.get("on-base_percentage") or player.get("on_base_percentage")),
                        safe_float(player.get("slugging_percentage")),
                        safe_float(player.get("on-base_plus_slugging") or player.get("on_base_plus_slugging")),
                        json.dumps(player)
                    )
                )
                inserted_id = cursor.fetchone()[0]
                conn.commit()
                logger.info(f"Stored player with id: {inserted_id}")
        logger.info(f"Successfully stored {len(players)} players")
        return True
    except Exception as e:
        logger.error(f"Database error: {e}")
        conn.rollback()
        return False

def fetch_paginated_players(conn, page: int, page_size: int) -> Dict[str, Any]:
    """
    Fetch paginated players from the database.
    """
    if not conn:
        logger.error("No database connection")
        return {}
    try:
        with conn.cursor() as cursor:
            offset = (page - 1) * page_size
            cursor.execute(
                "SELECT id, player_name, position, data FROM players LIMIT %s OFFSET %s",
                (page_size, offset)
            )
            records = cursor.fetchall()
            players_list = []
            for record in records:
                data_field = record[3]
                player_data = json.loads(data_field) if isinstance(data_field, str) else data_field
                players_list.append({
                    "id": record[0],
                    "player_name": record[1],
                    "position": record[2],
                    **player_data,
                })
            cursor.execute("SELECT COUNT(*) FROM players")
            total_players = cursor.fetchone()[0]
            total_pages = (total_players + page_size - 1) // page_size
            logger.info(f"Pagination: Total Players: {total_players}, Total Pages: {total_pages}")
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

def update_player(conn, player_id: int, player_data: Dict[str, Any]) -> bool:
    """
    Update a player's data in the database.
    """
    if not conn:
        logger.error("No database connection")
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE players SET data = %s WHERE id = %s",
                (json.dumps(player_data), player_id)
            )
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Database error: {e}")
        conn.rollback()
        return False