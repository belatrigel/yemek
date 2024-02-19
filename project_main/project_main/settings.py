"""
Django settings for project_main project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
#import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "accounts",
    "vendors",
    "menu",
    "marketplace",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_main.urls'
#print(os.path.join(BASE_DIR, "project_main","templates")) gerekirse bunu TEMPLATES/DIRS içinde kullan
      
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["project_main/templates",
                 "accounts/templates",
                 "jazzmin/templates",
                 "vendors/templates",
                 "menu/sablonlar",
                 "marketplace/temps",
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "vendors.context_processor.get_vendor",
            ],
        },
    },
]

WSGI_APPLICATION = 'project_main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config("ENGINE"),
        'NAME': config("NAME"),
        'USER': config("USER"),
        'PASSWORD': config("PASSWORD"),
        "HOST": config("HOST"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    "project_main/static",
    "jazzmin/static",
]
STATIC_ROOT = BASE_DIR /"static"

# media için ayarlayayım.
MEDIA_URL = "medias/"
MEDIA_ROOT = BASE_DIR /"media_files"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "accounts.User"

# sweetalert2 için soru işareti ekledim.
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    50: "question",
}

# JAZZMIN İÇİN ÖZEL ---------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "YETU", # tarayıcı favicon tarafındaki on hover olduğumdaki yazı kısmı
    "site_header": "Yazılım Envanteri Takip Uygulaması",
    "site_brand": "Kahramanlar", # menüdeki soldaki üst yazı
    "site_icon": "images/amblem.jpg", # favico kısmında yer alan küçük resim
    # Add your own branding here
    "site_logo": "images/wellcome_page.jpg", # hem login resmi hem de admin menü üstündeki resimdedir.
    "welcome_sign": "Yazılım Envanteri Takip Uygulamasına Hoş Geldiniz.", # login sayfasındaki mesaj
    # Copyright on the footer
    "copyright": "Dz.K.K.lığı",
    "user_avatar": "images/capa_avatar.png", # ne olduğunu bul
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Denkom", "url": "https://www.dzkk.tsk.tr/", "permissions": ["auth.view_user"]},
        {"name": "Ana Sayfa", "url": 'index', "permissions": ["auth.view_user"]},
        
        # model admin to link to (Permissions checked against model)
        #{"name": "Hesaplar", "model": "accounts.models.User"},
    ],

    # Custom links to append to app groups, keyed on app name
    """ "custom_links": {
        "accounts": [{
            "name": "deneme", 
            "url": 'index', 
            "icon": "fas fa-comments",
            "permissions": ["accounts.view_book"]
        }]
    } """

    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": False,
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "users.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file",
    },
    # # Icons that are used when one is not manually specified
    "default_icon_parents": "fa-sharp fa-solid fa-diagram-project fa-spin fa-lg", # menu icon
    "default_icon_children": "fa-sharp fa-solid fa-angles-right fa-shake fa-lg", # ben yaptım
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    # Uncomment this line once you create the bootstrap-dark.css file
    "custom_css": "jazzmin/css/my_css_jazmin.css",
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-navy",
    "accent": "accent-warning",
    "navbar": "navbar-navy navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cyborg",
    "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}

# elmek setup
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_TIMEOUT = 10
EMAIL_BACKEND = config("EMAIL_BACKEND")
DEFAULT_FROM_EMAIL = "Food Online Market Place <emergul13@gmail.com>"