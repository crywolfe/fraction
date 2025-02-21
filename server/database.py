import os
import time
import psycopg2
from psycopg2 import OperationalError
import logging

logger = logging.getLogger(__name__)

DB_URL = os.environ.get("DB_URL")

def create_connection():
    conn = None
    retries = 5
    delay = 2
    for attempt in range(retries):
        try:
            # Explicitly parse and log connection parameters
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(DB_URL)
            query_params = parse_qs(parsed_url.query)
            
            # Detailed logging of connection parameters
            logger.info(f"Attempting database connection (attempt {attempt + 1}/{retries}):")
            logger.info(f"Raw DB_URL: {DB_URL}")
            logger.info(f"Scheme: {parsed_url.scheme}")
            logger.info(f"Hostname: {parsed_url.hostname}")
            logger.info(f"Port: {parsed_url.port or 5432}")
            logger.info(f"Username: {parsed_url.username}")
            logger.info(f"Database: {parsed_url.path.lstrip('/')}")
            
            # Attempt connection with explicit parameters
            conn = psycopg2.connect(
                host=parsed_url.hostname,
                port=parsed_url.port or 5432,
                database=parsed_url.path.lstrip('/'),
                user=parsed_url.username,
                password=parsed_url.password
            )
            logger.info("Database connection successful")
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {type(e).__name__} - {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
    logger.error("Max retries reached. Database connection failed.")
    return None

def create_table(conn):
    if not conn:
        logger.error("No database connection to create table.")
        return
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
                data JSONB,  -- Store the rest of the player data as JSON
                UNIQUE (player_name, position)
            )
        """)
        conn.commit()
        logger.info("Table 'players' created successfully with unique constraint")
    except Exception as e:
        logger.error(f"The error '{e}' occurred")
        conn.rollback()

conn = create_connection()
if conn:
    create_table(conn)