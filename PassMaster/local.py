from .base import *

# Uncomment these lines to see the 404 and 500 pages
# Comment these lines to see debug info
# DEBUG = False
# ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

EMAIL_HOST_USER = 'testemail2081@gmail.com'  # this is a testing account
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'TandemTricycle'
EMAIL_PORT = 587