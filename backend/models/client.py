from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated, List

class ClientSignup(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=4)]

class ClientLogin(BaseModel):
    email: EmailStr
    password: str
    
class ClientResponse(BaseModel):
    id: str
    username: str
    email: str
    routes: List[str]
