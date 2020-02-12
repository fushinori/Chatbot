# This file is for generating a string session only
# Please copy and save the string session
# Note that you need to have api_id and api_hash set in config.ini before executing this
from pyrogram import Client

with Client(":memory:") as app:
    print(app.export_session_string())
