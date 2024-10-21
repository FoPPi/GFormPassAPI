import asyncpg
import logging
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

import re

class Postgres:
    def __init__(self, db_name: str, user: str, password: str, host: str = 'localhost', port: int = 5432):
        self._db_name: str = db_name
        self._user: str = user
        self._password: str = password
        self._host: str = host
        self._port: int = port
        self._pool: Optional[asyncpg.Pool] = None
        self._logger: logging.Logger = logging.getLogger(__name__)

    async def connect(self) -> None:
        try:
            self._pool = await asyncpg.create_pool(
                user=self._user,
                password=self._password,
                database=self._db_name,
                host=self._host,
                port=self._port
            )
            self._logger.info("Connected to the database successfully.")
        except Exception as e:
            self._logger.error(f"Failed to connect to the database: {str(e)}")
            raise

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._logger.info("Closed database connection.")

    @asynccontextmanager
    async def connection(self):
        if not self._pool:
            await self.connect()
        async with self._pool.acquire() as conn:
            try:
                yield conn
            except Exception as e:
                self._logger.error(f"Database operation failed: {str(e)}")
                raise

    async def insert_data(self, table_name: str, data: Dict[str, Any]) -> None:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(f'${i + 1}' for i in range(len(data)))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        async with self.connection() as conn:
            await conn.execute(query, *data.values())
        self._logger.info(f"Inserted data into {table_name}")

    async def update_data(self, table_name: str, data: Dict[str, Any], condition: str = '1=1') -> None:
        set_clause = ', '.join(f"{key} = ${i + 1}" for i, key in enumerate(data.keys()))
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

        async with self.connection() as conn:
            await conn.execute(query, *data.values())
        self._logger.info(f"Updated data in {table_name}")

    async def delete_data(self, table_name: str, condition: str) -> None:
        query = f"DELETE FROM {table_name} WHERE {condition}"

        async with self.connection() as conn:
            await conn.execute(query)
        self._logger.info(f"Deleted data from {table_name}")

    async def select_data(self, table_name: str, columns = '*', condition: str = '1=1') -> List[Dict[str, Any]]:
        column_list = ', '.join(columns) if isinstance(columns, list) else columns
        query = f"SELECT {column_list} FROM {table_name} WHERE {condition}"

        async with self.connection() as conn:
            result = await conn.fetch(query)
        self._logger.info(f"Selected data from {table_name}")
        return [dict(row) for row in result]

    async def execute_transaction(self, query: str) -> None:
        async with self.connection() as conn:
            async with conn.transaction():
                await conn.execute(query)
        self._logger.info("Executed transaction successfully")

    @staticmethod
    def to_pg_array(python_list: List[str]) -> str:
        escaped_items = [item.replace('"', '\\"') for item in python_list]
        return '{' + ','.join(f'"{item}"' for item in escaped_items) + '}'

    @staticmethod
    def extract_pg_array(pg_array_string: str) -> list:
        # Remove the outer braces
        content = pg_array_string.strip()[1:-1]

        # Split the content by commas, but not commas within quotes
        pattern = r',\s*(?=(?:[^"]*"[^"]*")*[^"]*$)'
        elements = re.split(pattern, content)

        # Remove quotes from each element and strip whitespace
        return [element.strip().strip('"') for element in elements]

    # Query builder methods can be added here

    # Additional utility methods can be added here