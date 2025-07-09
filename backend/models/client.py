from pydantic import BaseModel, EmailStr, Field
from typing import Optional
class Client(BaseModel):
    id: int
    username: str
    email: EmailStr
    api_key: str
    password: str  
    
class ClientSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
class ClientLogin(BaseModel):
    email: EmailStr
    password: str