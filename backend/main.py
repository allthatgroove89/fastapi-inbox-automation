from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.read_email import router as read_email_router
from routes.email_list import router as email_list_router
from routes.delete_email import router as email_delete_router
from routes.email_connect import router as email_connect_router
from routes.email_labels import router as email_labels_router
from routes.dashboard import router as dashboard_router
from utils.rate_limiter import limiter, rate_limit_handler
from utils.logging import setup_logging
from slowapi.errors import RateLimitExceeded

app = FastAPI()
setup_logging()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server or Nginx container
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI backend is alive and routing correctly"}

app.include_router(read_email_router, prefix="/api")
app.include_router(email_list_router, prefix="/api")
app.include_router(email_delete_router, prefix="/api")
app.include_router(email_connect_router, prefix="/api")
app.include_router(email_labels_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")