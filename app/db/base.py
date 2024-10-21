import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger
from app.libs.postgres import Postgres

db: Postgres =  Postgres(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            db_name=settings.POSTGRES_DB,
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database
    failed_connections: int = 0
    while failed_connections < 10:
        try:
            logger.info("Connecting to the database...")
            await db.connect()
            logger.info("Connected to the database.")
            break
        except Exception as e:
            failed_connections += 1
            # logger.error(f"Failed to connect to the database: {e}. (attempt {failed_connections})") # In postgres lib logs to stderr
            await asyncio.sleep(1)  # Non-blocking sleep for async context

    if failed_connections > 10:
        logger.error("Failed to connect to the database 10 times. Exiting.")
        raise

    try:
        logger.info("Initializing database...")
        logger.info("Get script path...")
        # Get the directory containing the current script
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        # Use os.path.join to create the correct path to init_db.sql
        sql_script_path = os.path.join(CURRENT_DIR, "init_db.sql")
        logger.info(f"Script path: {sql_script_path}")
        logger.info("Read SQL script...")
        # Read the SQL script
        with open(sql_script_path, 'r') as file:
            sql_script = file.read()
            logger.debug(sql_script)
        logger.info("SQL script read.")

        logger.info("Execute SQL script...")
        # Execute the initialization script
        await db.execute_transaction(sql_script)

        logger.info("Database initialized.")
        yield
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise

