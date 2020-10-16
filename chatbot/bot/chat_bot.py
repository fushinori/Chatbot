from time import time
from pyrogram import filters, Client
from pyrogram.types import Message

from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
from coffeehouse.exception import CoffeeHouseError as CFError

from chatbot import app, LOGGER, CF_API_KEY, NAME
import chatbot.bot.database.chatbot_db as db


CoffeeHouseAPI = API(CF_API_KEY)
api_client = LydiaAI(CoffeeHouseAPI)


HELP_TEXT = """• Reply `.adduser` to someone to enable the chatbot for that person!
• Reply `.rmuser` to someone to stop the chatbot for them!
Have fun!"""

@app.on_message(filters.me & filters.command("start", "."))
async def start(_, message: Message) -> None:
    """Check if bot is up."""
    await message.edit_text("I'm alive! :3")


@app.on_message(filters.me & filters.command("help", "."))
async def help(_, message: Message) -> None:
    """Gives help on how to use the bot."""
    await message.edit_text(HELP_TEXT, parse_mode="md")
    
  
@app.on_message(filters.me & filters.command("adduser", "."))
async def add_user(_, message: Message) -> None:
    """Enable AI for a user."""
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
        await message.edit_text("AI enabled for user successfully!")
        LOGGER.info(f"AI enabled for user - {user_id}")
    else:
        await message.edit_text("AI is already enabled for this user!")
        

@app.on_message(filters.me & filters.command("rmuser", "."))
async def rem_user(_, message: Message) -> None:
    """Remove AI for a user."""
    if not message.reply_to_message:
        message.edit_text("You've gotta reply to someone!")
        return
    user_id = message.reply_to_message.from_user.id
    is_user = db.is_user(user_id)
    if not is_user:
        await message.edit_text("AI isn't enabled for this user in the first place!")
    else:
        db.rem_user(user_id)
        await message.edit_text("AI disabled for this user successfully!")
        LOGGER.info(f"AI disabled for user - {user_id}")


def check_message(msg: Message) -> bool:
    """Check if a message needs to be replied to."""
    reply_msg = msg.reply_to_message
    if NAME.lower() in msg.text.lower():
        return True
    if reply_msg and reply_msg.from_user is not None:
        if reply_msg.from_user.is_self:
            return True
    return False
    
        
@app.on_message(filters.text)
async def chatbot(app: Client, message: Message) -> None:
    msg = message
    if not check_message(msg):
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
        await msg.reply_chat_action("typing")
        response = api_client.think_thought(sesh, query)
        await msg.reply_text(response)
    except CFError as e:
        await app.send_message(chat_id=msg.chat.id, text=f"An error occurred:\n`{e}`", parse_mode="md")
