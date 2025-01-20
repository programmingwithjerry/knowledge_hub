from .base import *  # Import all settings from the base settings file

# Disable debug mode for production (DEBUG should be False in production for security and performance reasons)
DEBUG = False

# Define a list of admins who will be notified of errors via email
ADMINS = [
    ('Antonio M', 'email@mydomain.com'),  # Example admin contact, replace with actual admin details
]

# List of allowed hosts for the Django app. The '*' wildcard allows all hosts to access the app.
# In a production environment, this should be restricted to specific domain names for security.
ALLOWED_HOSTS = ['*']

# Database configuration for the SQLite database
DATABASES = {
    'default': {
        # Specifies the database engine; here it's SQLite
        'ENGINE': 'django.db.backends.sqlite3',

        # Defines the database name, which is stored in the BASE_DIR directory
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to the SQLite database file
    }
}

