import httpx
from typing import List, Dict, Any
from logging_config import logger


def standardize_player_keys(players: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Standardize player dictionary keys to snake_case.

    Args:
        players: List of player dictionaries

    Returns:
        List of players with standardized keys
    """
    return [
        {k.lower().replace(" ", "_"): v for k, v in player.items()}
        for player in players
    ]


async def fetch_external_players() -> List[Dict[str, Any]]:
    """
    Fetch players from external API.

    Returns:
        List of players or empty list if fetch fails
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.hirefraction.com/api/test/baseball"
            )
            response.raise_for_status()
            players = response.json()
            return standardize_player_keys(players)
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request Error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error fetching players: {e}")

        return []
