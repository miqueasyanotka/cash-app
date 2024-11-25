import environ
import os
from pathlib import Path
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Apartado configuración con variables de entornos
env = environ.Env()
env_file = os.path.join(os.path.dirname(BASE_DIR), ".env")

env.read_env(env_file=env_file, overwrite=True)

SECRET_KEY_DEFAULT = 'django-insecure-2^e$jy#3%^7)5cv5mt*=#=s_!#m90%2!!vd5575$*296&f*4yg'

SECRET_KEY = env("SECRET_KEY", default=SECRET_KEY_DEFAULT)

DEBUG = env.bool('DJANGO_DEBUG', default=True)

ENVIRONMENT_RUN = env("ENVIRONMENT_RUN", default="local")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=['*'])
# fin apartado entorno






# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-2^e$jy#3%^7)5cv5mt*=#=s_!#m90%2!!vd5575$*296&f*4yg'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.usuarios',
    'apps.transacciones',

]

THIRD_APPS = []
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_APPS

AUTH_USER_MODEL = 'usuarios.Usuario'

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('inicio')




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': ['templates'],
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DEFAULT_DB_NAME = env("POSTGRES_DB")
DEFAULT_DB_USER = env("POSTGRES_USER")
DEFAULT_DB_HOST = env("POSTGRES_HOST")
DEFAULT_DB_PORT = env("POSTGRES_PORT")

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': DEFAULT_DB_NAME,
#         'USER': DEFAULT_DB_USER,
#         'PASSWORD': env("POSTGRES_PASSWORD"),
#         'HOST': DEFAULT_DB_HOST,
#         'PORT': DEFAULT_DB_PORT,
#         'ATOMIC_REQUESTS': True,
#         'CONN_MAX_AGE': env.int("CONN_MAX_AGE", default=60)
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST"),
        'PORT': env("POSTGRES_PORT"),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': env.int("CONN_MAX_AGE", default=60)
    }
}






# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Contenido Media
RUTA_CARPETA_MEDIA = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"
MEDIA_ROOT = RUTA_CARPETA_MEDIA

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
