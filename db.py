from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from asyncio import get_event_loop

from typing import Optional, List


class User(Document):
    class Settings:
        name: str = "users"

    user_id: int
    accepted: Optional[bool] = False
    lines: Optional[List[str]] = []


async def init_db(db_uri: str, db_name: str) -> None:
    client = AsyncIOMotorClient(db_uri)
    client.get_io_loop = get_event_loop

    await init_beanie(
        database = client.get_database(db_name),
        document_models = [
            User
        ]
    )
