import os

CACHE_REDIS_CONFIGURATION = {
    "HOST": os.environ.get('CACHEREDIS_DEFAULT_HOSTNAME', 'redis'),
    "PORT": os.environ.get('CACHEREDIS_DEFAULT_PORT', 6379),
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            "SOCKET_TIMEOUT": 5,  # in seconds
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/code/images/dbsqlite/db.sqlite3'  # os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

ALLOWED_HOSTS = ['localhost', os.environ.get('LOCALHOST_MACHINE', '192.168.1.1'), '127.0.0.1']
INTERNAL_IPS = ('40.115.100.253', '130.192.85.198')
