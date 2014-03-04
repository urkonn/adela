import os
from settings import BASE_DIR

DEBUG = True

SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'sample.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


AWS_ACCESS_KEY_ID = ''

AWS_SECRET_ACCESS_KEY = ''

AWS_STORAGE_BUCKET_NAME = ''
