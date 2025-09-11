# FastAPI Inbox Automation

## Features
- FastAPI app exposing REST API
- React app served via Nginx
- PostgreSQL for the database
- Celery worker for background tasks
- Redis as broker for Celery
- Nginx reverse proxy for frontend and API routing
- Docker & docker-compose for orchestration

## Quick Start
1. Copy `.env` and adjust as needed
2. Build and start services:
   ```bash
   docker-compose up --build
   ```
3. Access API at [http://localhost:8000](http://localhost:8000)

## Endpoints
- `GET /` — Welcome message
- `POST /read-email/` — Add email reading task
- `GET /debug/emails` — List recent emails
- `POST /email/read` — Trigger email read task
- `POST /email/filter` — Apply spam filter

GET /email/stats — View spam/read stats
## Background Tasks
Celery worker will process email tasks using Redis as broker.
