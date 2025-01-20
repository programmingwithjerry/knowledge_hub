from .base import *  # Import all settings from the base settings file

# Enable debug mode for development (it should be set to False in production)
DEBUG = True

# Database configuration for the SQLite database
DATABASES = {
    'default': {
        # Specifies the database engine; here it's SQLite
        'ENGINE': 'django.db.backends.sqlite3',
        # Defines the database name, which is stored in the BASE_DIR directory
        # BASE_DIR is a path variable defined in the base settings file
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to the SQLite database file
    }
}

