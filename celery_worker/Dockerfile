FROM python:3.11-slim

WORKDIR /app

# Copy requirements from root
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Copy celery_worker directory contents
COPY celery_worker/ .

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
