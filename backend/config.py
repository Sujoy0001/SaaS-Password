import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = os.getenv("EXPIRE_MINUTES")



FRONTEND_URL = os.getenv("FRONTEND_URL")
# CORS origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    FRONTEND_URL
]
