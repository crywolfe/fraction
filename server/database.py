import os
import psycopg2
from psycopg2 import OperationalError
import logging

logger = logging.getLogger(__name__)

DB_URL = os.environ.get("DB_URL")

def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(DB_URL)
        logger.info("Database connection successful")
    except OperationalError as e:
        logger.error(f"The error '{e}' occurred")
    return conn

def create_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                player_name VARCHAR(255),
                position VARCHAR(255),
                games INTEGER,
                at_bat INTEGER,
                runs INTEGER,
                hits INTEGER,
                double_2b INTEGER,
                third_baseman INTEGER,
                home_run INTEGER,
                run_batted_in INTEGER,
                a_walk INTEGER,
                strikeouts INTEGER,
                stolen_base INTEGER,
                caught_stealing INTEGER,
                avg NUMERIC,
                on_base_percentage NUMERIC,
                slugging_percentage NUMERIC,
                on_base_plus_slugging NUMERIC,
                data JSONB  -- Store the rest of the player data as JSON
            )
        """)
        conn.commit()
        logger.info("Table 'players' created successfully")
    except Exception as e:
        logger.error(f"The error '{e}' occurred")

conn = create_connection()
if conn:
    create_table(conn)