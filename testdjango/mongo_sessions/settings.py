from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


MONGO_CLIENT = getattr(settings, 'MONGO_CLIENT', False)

MONGO_SESSIONS_COLLECTION = getattr(
    settings, 'MONGO_SESSIONS_COLLECTION', 'sessions'
)

# sessionid cookie will get different expiration time
MONGO_SESSIONS_TTL = getattr(
    settings, 'MONGO_SESSIONS_TTL', settings.SESSION_COOKIE_AGE
)

if not MONGO_CLIENT:
    MONGO_PORT = int(getattr(settings, 'MONGO_PORT', 27017))
    MONGO_HOST = getattr(settings, 'MONGO_HOST', 'localhost')
    MONGO_DB_NAME = getattr(settings, 'MONGO_DB_NAME', 'users')
    MONGO_DB_USER = getattr(settings, 'MONGO_DB_USER', False)
    MONGO_DB_PASSWORD = getattr(settings, 'MONGO_DB_PASSWORD', False)

    from pymongo import MongoClient

    MONGO_CLIENT = MongoClient(
        host=MONGO_HOST,
        port=MONGO_PORT,
    )

    MONGO_CLIENT = MONGO_CLIENT[MONGO_DB_NAME]

    if MONGO_DB_USER and MONGO_DB_PASSWORD:
        MONGO_CLIENT.authenticate(MONGO_DB_USER, MONGO_DB_PASSWORD)


DB_COLLECTION = MONGO_CLIENT[MONGO_SESSIONS_COLLECTION]

MONGO_SESSIONS_INDEXES = DB_COLLECTION.index_information()

# check existing indexes
if len(MONGO_SESSIONS_INDEXES) <= 1:
    DB_COLLECTION.ensure_index(
        'session_key',
        unique=True
    )

