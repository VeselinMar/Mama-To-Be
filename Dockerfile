FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev build-essential nginx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python3 manage.py collectstatic --noinput

# Expose port
EXPOSE 8000
EXPOSE 80

# Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Run Gunicorn as a non-root user (optional, recommended for security)
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Start Nginx and Gunicorn together
CMD service nginx start && gunicorn --bind 0.0.0.0:8000 mama_to_be.wsgi:application
