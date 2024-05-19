# Use a base image compatible with your Raspberry Pi's architecture
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Set up nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 80

# Start nginx and gunicorn
CMD service nginx start && gunicorn --bind 0.0.0.0:8000 wsgi:app
