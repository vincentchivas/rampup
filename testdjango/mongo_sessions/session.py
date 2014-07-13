import datetime

try:
    from django.utils.encoding import force_unicode
except ImportError:  # Python 3.*
    from django.utils.encoding import force_text as force_unicode
from django.contrib.sessions.backends.base import SessionBase, CreateError
from mongo_sessions import settings


class SessionStore(SessionBase):
    '''
    mongodb as Django sessions backend
    '''
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

        self.db_collection = settings.DB_COLLECTION
   # def get_expiration_date(self):
   #     return timezone.now() - timedelta(
   #        seconds=MONGO_SESSIONS_TTL
   #     )

    def load(self):
        mongo_session = self.db_collection.find_one({
            'session_key': self._get_or_create_session_key(),
            'expire_date': {
                '$gt': datetime.datetime.now()
            }
        })

        if not mongo_session is None:
            return self.decode(force_unicode(mongo_session['session_data']))
        else:
            self.create()
            return {}

    def exists(self, session_key):
        session = self.db_collection.find_one({
            'session_key': session_key,
        })

        if session is None:
            return False
        else:
            # mongodb ttl invalidation runs only once per minute, delete manually
            if session['creation_date'] <= self.get_expiration_date():
                self.delete(session_key)
                return self.exists(session_key)
            return True

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            # ensure that session key is unique
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            return

    def save(self, must_create=False):
        session_key = self._get_or_create_session_key()
        if must_create and self.exists(session_key):
            raise CreateError

        session = {
            'session_key': session_key,
            'session_data': self.encode(
                self._get_session(no_load=must_create)
            ),
            'expire_date': self.get_expiry_date(),
        }

        self.db_collection.update(
            {'session_key': session_key},
            {'$set': session},
            upsert=True,
            safe=True
        )

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self.session_key
        self.db_collection.remove({'session_key': session_key})

    def set_expiry(self, value):
        raise NotImplementedError
