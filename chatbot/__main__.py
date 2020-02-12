import sys
from pyrogram.errors import RPCError
from chatbot import app, LOGGER

try:
    app.start()
except RPCError as e:
    LOGGER.error(str(e))
    exit(1)

app.stop()

from chatbot.bot import chat_bot

LOGGER.info("Simple chatbot written using the pyrogram library.\n " \
"Uses Intellivoid's Coffeehouse API.\n" \
"Written by @TheRealPhoenix on Telegram.")
LOGGER.info("Your bot is now online. Check .help for help!")

app.run()
