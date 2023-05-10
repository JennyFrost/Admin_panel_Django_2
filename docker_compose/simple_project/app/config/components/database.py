import os

from config.components.constants import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("DB_ENGINE"),
        'NAME': os.environ.get("DB_NAME"),
        # 'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
        'USER': os.environ.get('DB_USER', 'user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
           'options': '-c search_path=public,content'
        }
    }
}

