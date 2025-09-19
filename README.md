# FastAPI Inbox Automation

## Features
- FastAPI app exposing REST API for email automation
- React dashboard served via Nginx
- PostgreSQL for persistent email storage
- Celery worker for background email and spam processing
- Redis as broker for Celery
- Nginx reverse proxy for frontend and API routing
- Docker & docker-compose for orchestration
- User authentication (dummy for now, Personal credentials local-only, extendable)
- IMAP integration (Gmail-ready, configurable via .env)
- Inbox/Spam filtering and stats
- Modular backend with extensible routes (labels, inbox, debug, etc.)
- Modern, mobile-friendly dashboard UI with sidebar stats, filters, and pagination
- User model supports passing `email_password` (not just .env)

## Quick Start
1. Copy `.env` and adjust as needed (see example in repo)
2. Build and start all services:
   ```bash
   docker-compose up --build
   ```
3. Access the dashboard at [http://localhost:8000](http://localhost:8000)
4. API root at [http://localhost:8000/api](http://localhost:8000/api)

## Deployment

- Production deployments use AWS EC2 with an Elastic IP for stable public access.
- After deploying, access your app at `http://98.88.137.102:8000` (or your configured port).
- Make sure your EC2 security group allows inbound traffic on the necessary ports (e.g., 80, 443, 8000).
- Update your DNS records if you want to use a custom domain.

## Gmail IMAP Setup
- To access spam via IMAP, you must enable the label `[Gmail]/Spam` in Gmail:
  - Go to Gmail → Settings → Labels → Find "Spam" and check "Show in IMAP".

## Main Endpoints
- `GET /api/` — Welcome message
- `GET /api/email/list` — Paginated, filterable email list (supports `spam`, `search`, `older_than`, etc.)
- `GET /api/email/inbox` — Fetch inbox emails for current user (dummy auth)
  - Supports `folder` query param, e.g.:
    ```bash
    GET /api/email/inbox?folder="[Gmail]/Spam"
    ```
- `POST /api/email/read` — Trigger email read task
- `POST /api/email/filter` — Run spam filter on all emails and update spam status (returns summary)
- `POST /auth/logout` — Log out the current user (dummy endpoint, clears session on frontend)
- `GET /api/email/stats` — View spam/read stats
- `GET /api/dashboard` — Dashboard stats (total, spam, unread, recent)
- `GET /api/email/labels` — List available email labels
- `GET /api/debug/emails` — List recent emails (debug)
- `POST /api/read-email/` — Add email reading task

## Frontend Features
- Minimal, mobile-friendly React dashboard
- Sidebar with live stats (total, spam, unread, recent)
- Inbox/Spam toggle and search/filter controls
- Paginated email list with collapsible sections (Inbox, Spam, etc.)
- Animated button and card hover effects
- Accessible forms and keyboard navigation

## Background Tasks
- Celery worker processes email and spam tasks using Redis as broker
- Automatic email reading and spam detection (extendable)

## Development Notes
- User authentication is currently a dummy function; extend `get_current_user` for real auth
- IMAP credentials are loaded from `.env` (see `backend/imap_config.py`) or passed via the User model
- To avoid port conflicts, ensure no other service is using port 5432 (Postgres)
- For custom IMAP or user logic, update `backend/services/email.py`

---
For more details, see the code and comments in each module. PRs and issues welcome!

---
**Author/Collaborator:** Saul Vera Echevestre  
Email: saul.vera787@gmail.com
