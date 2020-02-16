import sys
from chatbot import app, LOGGER

from chatbot.bot import chat_bot

if len(sys.argv) not in (1, 3, 4):
    quit(1)
else:
    app.start()
    LOGGER.info("Simple chatbot written using the pyrogram library.\n " \
    "Uses Intellivoid's Coffeehouse API.\n" \
    "Written by @TheRealPhoenix on Telegram.")
    LOGGER.info("Your bot is now online. Check .help for help!")
    app.idle()
