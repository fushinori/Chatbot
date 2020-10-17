import asyncio
import importlib

from pyrogram import idle
from chatbot import app, LOGGER


importlib.import_module("chatbot.bot.chat_bot")


async def start_bot() -> None:
    await app.start()
    LOGGER.info(
        "Simple chatbot written using the pyrogram library.\n "
        "Uses Intellivoid's Coffeehouse API.\n"
        "Written by @TheRealPhoenix on Telegram."
    )
    LOGGER.info("Your bot is now online. Check .help for help!")
    await idle()

asyncio.get_event_loop().run_until_complete(start_bot())
