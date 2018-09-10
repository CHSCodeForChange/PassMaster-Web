from .base import *
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ['DEBUG'].lower() in ['true', 't', 'yes', 'y']:
	DEBUG = True
else:
	DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
	}
}

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_PORT = 587