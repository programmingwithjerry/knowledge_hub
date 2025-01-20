from decouple import config
from .base import *  # Import all settings from the base settings file

# Disable debug mode for production (DEBUG should be False in production for security and performance reasons)
DEBUG = False

# Define a list of admins who will be notified of errors via email
ADMINS = [
    ('eneyellow', 'eneyellowj@gmail.com'),  # Example admin contact, replace with actual admin details
]

# List of allowed hosts for the Django app. The '*' wildcard allows all hosts to access the app.
# In a production environment, this should be restricted to specific domain names for security.
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Database configuration for the postgresql database
DATABASES = {
    # Default database configuration
    'default': {
        # Specify the database engine to be used; here, it's PostgreSQL
        'ENGINE': 'django.db.backends.postgresql',

        # Database name retrieved from environment variables via the `config` function
        'NAME': config('POSTGRES_DB'),

        # Username for the database, also retrieved from environment variables
        'USER': config('POSTGRES_USER'),

        # Password for the database, securely loaded from environment variables
        'PASSWORD': config('POSTGRES_PASSWORD'),

        # Hostname for the database service; 'db' refers to the Docker service name
        'HOST': 'db',

        # Port number on which the database service is listening
        'PORT': 5432,
    }
}
