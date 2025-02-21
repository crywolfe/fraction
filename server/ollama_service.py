import ollama
import random
import json
import os
from logging_config import logger
from typing import Dict, Any

# Configure Ollama client with host from environment
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
ollama.host = OLLAMA_HOST
logger.info(f"Configured Ollama with host: {OLLAMA_HOST}")


def generate_player_description(
    player_name: str, position: str, team: str, player_data: Dict[str, Any]
) -> str:
    """
    Generate a concise player description using Ollama.

    Args:
        player_name: Name of the player
        position: Player's position
        team: Player's team
        player_data: Additional player data

    Returns:
        Generated player description
    """
    prompt = (
        f"Generate a concise 280-character description for a baseball player with these details:\n"
        f"Name: {player_name}\n"
        f"Position: {position}\n"
        f"Team: {team}\n\n"
        f"Include career highlights, playing style, and personal background."
    )
    logger.info("Preparing to generate description")
    logger.info("Ollama Model: llama3.2:1b")
    logger.info(f"Full Prompt: {prompt}")

    try:
        chat_params = {
            "model": "llama3.2:1b",
            "messages": [{"role": "user", "content": prompt}],
        }
        logger.info(f"Chat Call Parameters: {chat_params}")
        response = ollama.chat(**chat_params)
        message_content = response.get("message", {}).get("content", "")
        description = message_content[:280]
        logger.info(f"Generated Description (Length {len(description)}): {description}")

        if not description:
            logger.warning("Empty description generated")
            return generate_fallback_description(position, team, player_data)

        return description
    except Exception as e:
        logger.error(f"Ollama generation error: {e}")
        logger.exception("Detailed Ollama generation error")
        return generate_fallback_description(position, team, player_data)


def generate_fallback_description(
    position: str, team: str, player_data: Dict[str, Any]
) -> str:
    """
    Generate a fallback description when Ollama generation fails.

    Args:
        position: Player's position
        team: Player's team
        player_data: Additional player data

    Returns:
        Fallback description
    """
    fallback_descriptions = [
        f"A talented {position} with a passion for the game.",
        f"Bringing skill and determination to {team}.",
        "A rising star in baseball, known for precision and teamwork.",
    ]
    return random.choice(fallback_descriptions)
