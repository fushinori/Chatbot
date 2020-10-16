import os
import sys
import logging

from pyrogram import Client

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# If python version < 3.6, quit
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("You need at least python v3.6.x\nBot quitting.")
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    SESSION_NAME = os.environ.get("SESSION_NAME")
    STRING_SESSION = os.environ.get("STRING_SESSION")
    CF_API_KEY = os.environ.get("CF_API_KEY")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    NAME = os.environ.get("NAME")
    
else:
    from configparser import ConfigParser
    
    parser = ConfigParser()
    parser.read("config.ini")
    config = parser["config"]
    
    SESSION_NAME = config.get("SESSION_NAME")
    STRING_SESSION = config.get("STRING_SESSION")
    CF_API_KEY = config.get("CF_API_KEY")
    DATABASE_URL = config.get("DATABASE_URL")
    NAME = config.get("NAME")

if not SESSION_NAME and not STRING_SESSION:
    print("There's no session set up!")
    quit(1)
if SESSION_NAME:
    SESSION = SESSION_NAME
elif STRING_SESSION:
    SESSION = STRING_SESSION
app = Client(SESSION)
