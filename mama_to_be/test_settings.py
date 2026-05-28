from .settings import *

# --------------------------------------------------
# EMAIL: disable external SMTP completely in CI
# --------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

DEFAULT_FROM_EMAIL = "test@example.com"
CONTACT_RECEIVER_EMAIL = "test@example.com"

# Override Brevo-related settings safely (prevent import crash)
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False

# --------------------------------------------------
# STORAGE: local only
# --------------------------------------------------

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# --------------------------------------------------
# SECURITY: fast hashing for tests
# --------------------------------------------------

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# --------------------------------------------------
# CACHE: in-memory (important for your token logic)
# --------------------------------------------------

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# --------------------------------------------------
# RATELIMIT: disable or relax in CI
# --------------------------------------------------

RATELIMIT_ENABLE = False