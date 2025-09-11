from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.read_email import router as read_email_router
from routes.email_list import router as email_list_router
from routes.delete_email import router as email_delete_router
 
app = FastAPI()

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

app.include_router(read_email_router)
app.include_router(email_list_router)
app.include_router(email_delete_router)
