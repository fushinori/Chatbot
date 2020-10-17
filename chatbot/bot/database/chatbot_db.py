import threading

from sqlalchemy import Column, String, Integer

from chatbot.bot.database import BASE, SESSION


class Chatbot(BASE):
    __tablename__ = "chatbot"
    user_id = Column(Integer, primary_key=True)
    ses_id = Column(String(64))
    expires = Column(String(10))

    def __init__(self, user_id, ses_id, expires):
        self.user_id = user_id
        self.ses_id = ses_id
        self.expires = expires


Chatbot.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()
USERS = set()


def is_user(user_id):
    try:
        user = SESSION.query(Chatbot).get(int(user_id))
        if user:
            return True
        else:
            return False
    finally:
        SESSION.close()


def set_ses(user_id, ses_id, expires):
    with INSERTION_LOCK:
        autochat = SESSION.query(Chatbot).get(int(user_id))
        if not autochat:
            autochat = Chatbot(int(user_id), str(ses_id), str(expires))
        else:
            autochat.ses_id = str(ses_id)
            autochat.expires = str(expires)

        SESSION.add(autochat)
        SESSION.commit()
        __load_userid_list()


def get_ses(user_id):
    autochat = SESSION.query(Chatbot).get(int(user_id))
    sesh = ""
    exp = ""
    if autochat:
        sesh = str(autochat.ses_id)
        exp = str(autochat.expires)

    SESSION.close()
    return sesh, exp


def rem_user(user_id):
    with INSERTION_LOCK:
        autochat = SESSION.query(Chatbot).get(int(user_id))
        if autochat:
            SESSION.delete(autochat)

        SESSION.commit()
        __load_userid_list()


def __load_userid_list():
    global USERS
    try:
        USERS = {int(x.user_id) for x in SESSION.query(Chatbot).all()}
    finally:
        SESSION.close()


__load_userid_list()
