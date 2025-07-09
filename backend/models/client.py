from pydantic import BaseModel, EmailStr, Field
from typing import Optional
class Client(BaseModel):
    id: int
    username: str
    email: EmailStr
    api_key: str
    profile_img: Optional[str] = None
    password: str  
class ClientLogin(BaseModel):
    email: EmailStr
    password: str