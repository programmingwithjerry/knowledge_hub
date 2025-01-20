# Use the official Python 3.12.3 image as the base image for the Docker container
FROM python:3.10.12

# Set environment variables to improve Python behavior in the container
# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is not buffered (helpful for logging in real-time in containers)
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container to /code
# All subsequent commands will be run relative to this directory
WORKDIR /code

# Upgrade pip to ensure the latest version is installed before installing dependencies
RUN pip install --upgrade pip

# Copy the requirements.txt file to the working directory (/code)
COPY requirements.txt .

# Install Python dependencies from the requirements.txt file
RUN pip install -r requirements.txt

# Copy the entire Django project (and other files) into the container's working directory
COPY . .
