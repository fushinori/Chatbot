import sys
from pyrogram.errors import RPCError
from chatbot import app, LOGGER
from chatbot.bot import chat_bot

try:
    app.run()
except RPCError as e:
    LOGGER.error(str(e))
    exit(1)
    
LOGGER.info("Simple chatbot written using the pyrogram library.\n " \
"Uses Intellivoid's Coffeehouse API.\n" \
"Written by @TheRealPhoenix on Telegram.")
LOGGER.info("Your bot is now online. Check .help for help!")