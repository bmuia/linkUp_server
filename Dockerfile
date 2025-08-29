# Base image
FROM python:3.12-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run with Daphne (ASGI for WebSockets)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "ping_backend.asgi:application"]
