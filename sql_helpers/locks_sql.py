from sqlalchemy import Boolean, Column, String
from sql_helpers import SESSION, BASE


class Locks(BASE):
    __tablename__ = "locks"
    chat_id = Column(String(14), primary_key=True)
    # Booleans are for "is this locked", _NOT_ "is this allowed"
    url = Column(Boolean, default=False)
    bots = Column(Boolean, default=False)
    forward = Column(Boolean, default=False)
    commands = Column(Boolean, default=False)


    def __init__(self, chat_id):
        self.chat_id = str(chat_id)  # ensure string
        self.url = False
        self.bots = False
        self.forward = False
        self.commands = False


Locks.__table__.create(checkfirst=True)


def init_locks(chat_id, reset=False):
    curr_restr = SESSION.query(Locks).get(str(chat_id))
    if reset:
        SESSION.delete(curr_restr)
        SESSION.flush()
    restr = Locks(str(chat_id))
    SESSION.add(restr)
    SESSION.commit()
    return restr


def update_lock(chat_id, lock_type, locked):
    curr_perm = SESSION.query(Locks).get(str(chat_id))
    if not curr_perm:
        curr_perm = init_locks(chat_id)
    if lock_type == "url":
        curr_perm.url = locked
    elif lock_type == "bots":
        curr_perm.bots = locked
    elif lock_type == "forward":
        curr_perm.forward = locked
    elif lock_type == "commands":
        curr_perm.commands = locked
    SESSION.add(curr_perm)
    SESSION.commit()


def is_locked(chat_id, lock_type):
    curr_perm = SESSION.query(Locks).get(str(chat_id))
    SESSION.close()
    if not curr_perm:
        return False
    elif lock_type == "url":
        return curr_perm.url
    elif lock_type == "bots":
        return curr_perm.bots
    elif lock_type == "forward":
        return curr_perm.forward
    elif lock_type == "commands":
        return curr_perm.commands


def get_locks(chat_id):
    try:
        return SESSION.query(Locks).get(str(chat_id))
    finally:
        SESSION.close()
