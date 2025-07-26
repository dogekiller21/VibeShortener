FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install uv
RUN pip install --no-cache-dir uv

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Switch to user BEFORE installing dependencies
USER app
WORKDIR /home/app

# Copy only dependency files first for better layer caching
COPY --chown=app:app pyproject.toml uv.lock ./

# Install Python dependencies in user's home directory
RUN uv sync --python python3 --no-cache

# Switch back to app directory
WORKDIR /app

# Copy application code with correct ownership
COPY --chown=app:app src/ /app/src/
COPY --chown=app:app alembic/ /app/alembic/
COPY --chown=app:app alembic.ini /app/alembic.ini

# Activate virtual environment
ENV PATH="/home/app/.venv/bin:$PATH" 