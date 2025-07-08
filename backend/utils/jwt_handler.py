from datetime import datetime, timedelta
from jose import jwt

from config import SECRET_KEY, ALGORITHM, EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire_minutes = int(EXPIRE_MINUTES) if EXPIRE_MINUTES is not None else 15
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY must not be None")
    if ALGORITHM is None:
        raise ValueError("ALGORITHM must not be None")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    