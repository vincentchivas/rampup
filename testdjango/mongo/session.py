import datetime
from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.utils.encoding import force_unicode
from db.dbop import db

class SessionStore(SessionBase):
    """
    Implements MongoDB session store.
    """
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def load(self):
        print self.session_key
        s = db.sessions.find_one( {
                'session_key': self._get_or_create_session_key(),
                'expire_date': {'$gt': datetime.datetime.now()}})
        print s
        print datetime.datetime.now()
        if s:
            return self.decode(force_unicode(s['session_data']))
        else:
            self.create()
            return {}


    def exists(self, session_key):
        if db.sessions.find_one( {'session_key': session_key} ):
            return True
        else:
            return False
    def create(self):
        while True:
            self.session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self, must_create=False):
        """
        Saves the current session data to the database. If 'must_create' is
        True, a database error will be raised if the saving operation doesn't
        create a *new* entry (as opposed to possibly updating an existing
        entry).
        """
        session_key = self._get_or_create_session_key()
        if self.exists(session_key):
            raise  CreateError

        obj = {
            'session_key': self.session_key,
            'session_data': self.encode(self._get_session(no_load=must_create)),
            'expire_date': self.get_expiry_date(),
            }
        res = db.sessions.update(
                {'session_key': self.session_key},
                {'$set': obj},
                upsert=True,
                safe=True,
                )
        if res['err'] is not None and must_create:
            raise CreateError

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        db.sessions.remove({'session_key': session_key})
