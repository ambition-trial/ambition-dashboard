"""
Django settings for ambition_dashboard project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_NAME = 'ambition_dashboard'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ftblcrb__%!_r6nl_kn-*u(rwhfeakwv*)j4^%=ltvp&s9^@i9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SITE_ID = 10
REVIEWER_SITE_ID = 0


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_crypto_fields.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'edc_timepoint.apps.AppConfig',
    'edc_protocol.apps.AppConfig',
    'edc_device.apps.AppConfig',
    'edc_metadata.apps.AppConfig',
    'edc_navbar.apps.AppConfig',
    'edc_action_item.apps.AppConfig',
    'edc_lab.apps.AppConfig',
    'edc_lab_dashboard.apps.AppConfig',
    'edc_locator.apps.AppConfig',
    'edc_identifier.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'edc_model_wrapper.apps.AppConfig',
    'ambition_dashboard.apps.EdcAppointmentAppConfig',
    'ambition_dashboard.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'edc_subject_dashboard.middleware.DashboardMiddleware',
    'edc_dashboard.middleware.DashboardMiddleware',
    'edc_lab_dashboard.middleware.DashboardMiddleware']


ROOT_URLCONF = 'ambition_dashboard.urls'

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

WSGI_APPLICATION = 'ambition_dashboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
KEY_PATH = os.path.join(BASE_DIR, 'crypto_fields')
GIT_DIR = BASE_DIR

DASHBOARD_URL_NAMES = {
    'subject_listboard_url': 'ambition_dashboard:subject_listboard_url',
    'screening_listboard_url': 'ambition_dashboard:screening_listboard_url',
    'subject_dashboard_url': 'ambition_dashboard:subject_dashboard_url',
}

DASHBOARD_BASE_TEMPLATES = {
    'listboard_base_template': 'ambition/base.html',
    'dashboard_base_template': 'ambition/base.html',
    'screening_listboard_template': 'ambition_dashboard/screening/listboard.html',
    'subject_listboard_template': 'ambition_dashboard/subject/listboard.html',
    'subject_dashboard_template': 'ambition_dashboard/subject/dashboard.html',
}
LAB_DASHBOARD_REQUISITION_MODEL = 'ambition_dashboard.subjectrequisition'

if 'test' in sys.argv:

    class DisableMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher', )
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
