from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated, Dict, Literal

class ClientSignup(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=4)]

class ClientLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=4)]
    
    
class RouteDetail(BaseModel):
    url: str
    method: Literal["GET", "POST", "DELETE", "PUT", "PATCH", "None"]
    
class ClientResponse(BaseModel):
    id: str
    username: str
    email: str
    api_key: str
    routes: Dict[str, RouteDetail]
