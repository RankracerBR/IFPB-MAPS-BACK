FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    apt-get install build-dep python-psycopg2

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the port Django runs on
EXPOSE 8002

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8002", "configs.wsgi:application"]