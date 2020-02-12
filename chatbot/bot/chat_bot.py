from time import time
from pyrogram import Filters

import coffeehouse as cf
from coffeehouse.exception import CoffeeHouseError as CFError

from chatbot import app, LOGGER, CF_API_KEY, NAME
import chatbot.bot.database.chatbot_db as db

api_client = cf.API(CF_API_KEY)


HELP_TEXT = """• Reply `.adduser` to someone to enable the chatbot for that person!
• Reply `.rmuser` to someone to stop the chatbot for them!
Have fun!"""

@app.on_message(Filters.me & Filters.regex("^\.start$"))
def start(client, message):
    message.edit_text("I'm alive! :3")


@app.on_message(Filters.me & Filters.regex("^\.help$"))
def help(client, message):
    message.edit_text(HELP_TEXT, parse_mode="md")
    
  
@app.on_message(Filters.me & Filters.regex("^\.adduser$"))
def add_user(client, message):
    if not message.reply_to_message:
        message.edit_text("Reply to someone to enable chatbot for that person!")
        return
    user_id = message.reply_to_message.from_user.id
    is_user = db.is_user(user_id)
    if not is_user:
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        db.set_ses(user_id, ses_id, expires)
        message.edit_text("AI enabled for user successfully!")
        LOGGER.info(f"AI enabled for user - {user_id}")
    else:
        message.edit_text("AI is already enabled for this user!")
        

@app.on_message(Filters.me & Filters.regex("^\.rmuser$"))
def rem_user(client, message):
    if not message.reply_to_message:
        message.edit_text("You've gotta reply to someone!")
        return
    user_id = message.reply_to_message.from_user.id
    is_user = db.is_user(user_id)
    if not is_user:
        message.edit_text("AI isn't enabled for this user in the first place!")
    else:
        db.rem_user(user_id)
        message.edit_text("AI disabled for this user successfully!")
        LOGGER.info(f"AI disabled for user - {user_id}")


def check_message(client, msg):
    reply_msg = msg.reply_to_message
    if NAME.lower() in msg.text.lower():
        return True
    if reply_msg:
        if reply_msg.from_user.is_self:
            return True
    return False
    
        
@app.on_message(Filters.text)
def chatbot(client, message):
    msg = message
    if not check_message(client, msg):
        return
    user_id = msg.from_user.id
    if not user_id in db.USERS:
        return
    sesh, exp = db.get_ses(user_id)
    query = msg.text
    if int(exp) < time():
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        db.set_ses(user_id, ses_id, expires)
        sesh, exp = ses_id, expires
        
    try:
        msg.reply_chat_action("typing")
        response = api_client.think_thought(sesh, query)
        msg.reply_text(response)
    except CFError as e:
        app.send_message(chat_id=msg.chat.id, text=f"An error occurred:\n`{e}`", parse_mode="md")

app.run()