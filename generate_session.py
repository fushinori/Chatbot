# Generate session files for permanent session.
# Not suitable for ephemeral file systems like Heroku.
import asyncio
from pyrogram import Client

async def create_session() -> None:
    async with Client("Phoenix"):
        pass
             
asyncio.run(create_session())