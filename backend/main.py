from fastapi import FastAPI
from routes import auth_routes
from config import ALLOWED_ORIGINS

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {"message": "Welcome to fastapi backend"}

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])