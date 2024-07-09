# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install git and necessary build tools
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libssl-dev \
    && apt-get clean

# Set environment variables to prevent Python from writing .pyc files to disk
# and to buffer stdout and stderr so that it behaves like a regular program
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Run the application
CMD ["python3", "-m", "WebStreamer"]
