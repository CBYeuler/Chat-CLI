# Dockerfile
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage cache
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app and client into container
COPY app /app/app
COPY client /app/client

# Copy entrypoint script (optional)
COPY start_in_container.sh /app/start_in_container.sh
RUN chmod +x /app/start_in_container.sh

EXPOSE 8765

# Use the env variables in docker-compose to configure MONGO_URI, PORT etc.
CMD [ "bash", "/app/start_in_container.sh" ]
