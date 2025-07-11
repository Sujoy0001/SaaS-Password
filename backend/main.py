from fastapi import FastAPI
from routes import auth, show, user
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

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(show.router, tags=["Client"])
app.include_router(user.router, tags=["user"])
