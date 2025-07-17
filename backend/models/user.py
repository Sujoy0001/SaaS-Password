from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated

class UserSignup(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=4)]

class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=4)]

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
