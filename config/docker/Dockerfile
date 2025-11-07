# PhiGEN Docker Development Environment
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements if they exist
COPY requirements.txt* ./

# Install Python dependencies
RUN pip install --no-cache-dir \
    PyQt6 \
    cryptography \
    bandit \
    pylint \
    black \
    pytest \
    requests \
    flask \
    flask-cors \
    discord.py \
    anthropic \
    chromadb \
    sentence-transformers \
    || true

# Copy project files
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV QT_QPA_PLATFORM=offscreen

# Default command
CMD ["/bin/bash"]
