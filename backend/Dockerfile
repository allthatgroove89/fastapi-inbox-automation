FROM python:3.11-slim

# Set working directory to /backend
WORKDIR /backend

# Copy requirements from project root
COPY requirements.txt ./requirements.txt


# Copy backend code into /backend
COPY backend/ .
# Copy celery worker code into /backend/celery_worker
COPY celery_worker/ ./celery_worker/

# Debug: List contents to verify copy
RUN echo "\n--- /backend contents ---" && ls -l /backend && \
	echo "\n--- /backend/celery_worker contents ---" && ls -l /backend/celery_worker

# Ensure /backend and /backend/celery_worker are in PYTHONPATH
ENV PYTHONPATH="/backend:/backend/celery_worker:${PYTHONPATH}"

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
