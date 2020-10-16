# Generate session files for permanent session.
# Not suitable for ephemeral file systems like Heroku.
import asyncio
from pyrogram import Client


# Choose name for session
NAME = "Phoenix"

async def create_session() -> None:
    async with Client(NAME):
        pass
             
asyncio.run(create_session())
