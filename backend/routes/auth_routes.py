from fastapi import APIRouter, HTTPException
from models.client import Client
from db.database import client_collections
from utils.hash_pass import hash_password, verify_password
from utils.jwt_handler import create_access_token

router = APIRouter()


async def get_next_client_id():
    last_client = await client_collections.find_one(sort=[("id", -1)])
    return last_client["id"] + 1 if last_client else 1

@router.post("/register")
async def register(user: Client):
    if await client_collections.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    if await client_collections.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user_dict = user.dict()
    user_dict["id"] = await get_next_client_id()
    user_dict["password"] = hash_password(user.password)

    await client_collections.insert_one(user_dict)
    return {"message": "User registered successfully", "id": user_dict["id"]}



@router.post("/login")
async def login(email: str, password: str):
    user = await client_collections.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")

    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
    })

    return {
        "access_token": token,
        "token_type": "bearer",
    }