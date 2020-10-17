# This file is for generating a string session only
# Please copy and save the string session
# Note that you need to have api_id and api_hash set in config.ini before
# executing this
import asyncio

from pyrogram import Client


async def get_session() -> None:
    async with Client(":memory:") as bot:
        print(bot.export_session_string())

asyncio.run(get_session())
