from pydantic import BaseModel, EmailStr
from typing import Optional

class client(BaseModel):
    id: int
    userName: str
    email: EmailStr
    profile_img: Optional[str] = None
    password: str
    
class Login(BaseModel):
    email: EmailStr
    password: str