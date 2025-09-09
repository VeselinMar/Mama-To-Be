# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port Render uses
EXPOSE 10000

# Entry point: run migrations, collect static, then start Gunicorn
CMD sh -c "\
    python manage.py migrate --noinput && \
    if [ -f seed.json ]; then python manage.py seed || true; fi && \
    python manage.py collectstatic --noinput && \
    python manage.py create_missing_profiles && \
    gunicorn --bind 0.0.0.0:10000 mama_to_be.wsgi:application"