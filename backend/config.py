import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = os.getenv("EXPIRE_MINUTES")

BACKEND_URL = os.getenv("BACKEND_URL")

FRONTEND_URL = os.getenv("FRONTEND_URL")