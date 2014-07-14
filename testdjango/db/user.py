from db.config import USER_DB
from model.user import User
from db.seqid import get_next_id


def save_user(user):
    assert user
    if not user._id:
        # assign sequential id
        user._id = get_next_id('user')
    USER_DB.user.save(user)
    return user

def find_one_user(filters={}):
    item=USER_DB.user.find_one(filters)
    return item

def del_user(user_id):
    assert user_id
    status=0
    if user_id:
        USER_DB.user.remove({'_id':user_id})
        status=1
    return status

def find_users(filters={}):
    users={}
    items=USER_DB.user.find(filters)
    for item in items:
        uid=item['_id']
        users[uid]=item
    return users

def find_session(filters={}):
    item=USER_DB.sessions.find_one(filters)
    return item
