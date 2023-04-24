from .core_settings import *


# debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# Email configuration for authentication
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'