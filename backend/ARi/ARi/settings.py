"""
Django settings for ARi project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/
 
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import ldap3
import sys
from .utils import ImperialDoCSpecifics
from ldap3.utils.conv import escape_filter_chars

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*hwb&#(m8&$a8fyq*-=#u7h14tb!e)fkk#c3%17im@1*&+4w)0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ari-server.herokuapp.com',
                 'localhost',
                 '127.0.0.1',
                 '146.169.45.4']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'planner',
    'login',
    'courses',

    # Django Packages
    'rest_framework',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Config
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'ARi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ARi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# NOTE: These settings are for development only. Move to CSG database for
# deployment

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'g1627132_u',
        'USER': 'g1627132_u',
        'PASSWORD': 'JNZdJ3JuFB',
        'HOST': 'db.doc.ic.ac.uk',
        'PORT': '5432',
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'g1627132_u',
        'USER': 'harry',
        'PASSWORD': 'iamonlyaman',
        'HOST': '',
        'PORT': '5432',
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

# Django Auth Ldap
main_dn = 'DC=ic,DC=ac,DC=uk'
groups_dn = 'OU=Distribution,OU=Groups,OU=Imperial College \\28London\\29,' \
            ''+main_dn
users_dn = 'OU=doc,OU=Users,'+main_dn

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap3.backends.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend'
)

AUTH_LDAP_URI = 'ldaps://ldaps-vip.cc.ic.ac.uk:636'
AUTH_LDAP_BASE_DN = main_dn
AUTH_LDAP_BIND_TEMPLATE = 'CN={username},OU=doc,OU=Users,OU=Imperial College ' \
                          '(London),{base_dn}'
AUTH_LDAP_UID_ATTRIB = 'cn'
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
}
AUTH_PROFILE_MODULE = 'login.ARiProfile'
AUTH_LDAP_GROUP_MAP = {
    'CN=doc-all-first-year,'+groups_dn: ('c1',),
    'CN=doc-all-second-year,'+groups_dn: ('c2',),
    'CN=doc-all-third-year,'+groups_dn: ('c3',),
    'CN=doc-all-fourth-year,'+groups_dn: ('c4',),
    'CN=doc-students-223,'+groups_dn: ('Concurrency',),
    'CN=doc-students-210,'+groups_dn: ('Architecture',),
    'CN=doc-students-202,'+groups_dn: ('Algorithms',),
    'CN=doc-students-220,'+groups_dn: ('Design',),
    'CN=doc-students-221,'+groups_dn: ('Compilers',),
    'CN=doc-students-211,'+groups_dn: ('Operating Systems',),
    'CN=doc-students-212,'+groups_dn: ('Networks',),
    'CN=doc-students-231,'+groups_dn: ('Intro to AI',),
    'CN=doc-students-233,'+groups_dn: ('Computational Techniques',),
    'CN=doc-students-240,'+groups_dn: ('Models of Computation',),
    'CN=doc-students-245,'+groups_dn: ('Statistics',),
    'CN=doc-students-261,'+groups_dn: ('Laboratory 2',),
    'CN=doc-students-271,'+groups_dn: ('Web Apps',),
    'CN=doc-students-272,'+groups_dn: ('Team Skills',),
    'CN=doc-students-275,'+groups_dn: ('C++',),
    'CN=doc-students-276,'+groups_dn: ('Prolog',),
}


# JWT (Token) authentication
# https://getblimp.github.io/django-rest-framework-jwt/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
