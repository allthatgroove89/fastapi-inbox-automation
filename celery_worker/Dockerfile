FROM python:3.11-slim

WORKDIR /app

# Copy requirements from root
COPY requirements.txt ./requirements.txt


# Copy celery_worker and backend into /app
COPY celery_worker/ ./celery_worker/
COPY ../backend/ ./backend/

# Ensure /app and /app/backend are in PYTHONPATH for cross-package imports
ENV PYTHONPATH="/app:/app/backend:${PYTHONPATH}"

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "celery_worker.tasks", "worker", "--loglevel=info"]
