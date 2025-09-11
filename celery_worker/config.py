import os
from pathlib import Path

try:
	from dotenv import load_dotenv
	# try to load project-level .env (one level above this package)
	_env_path = Path(__file__).resolve().parents[1] / ".env"
	if _env_path.exists():
		load_dotenv(dotenv_path=str(_env_path))
except Exception:
	# python-dotenv is optional; fall back to environment variables
	pass

# Celery / Redis configuration (defaults suitable for docker-compose)
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL") or "redis://redis:6379/0"
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND") or CELERY_BROKER_URL

# IMAP / email configuration (no defaults for credentials)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER")

def imap_config_present() -> bool:
	"""Return True when all IMAP credentials are available."""
	return bool(EMAIL_USER and EMAIL_PASS and IMAP_SERVER)

__all__ = [
	"CELERY_BROKER_URL",
	"CELERY_RESULT_BACKEND",
	"EMAIL_USER",
	"EMAIL_PASS",
	"IMAP_SERVER",
	"imap_config_present",
]

