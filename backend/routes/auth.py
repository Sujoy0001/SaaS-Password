from fastapi import APIRouter, HTTPException
from models.client import ClientSignup, ClientLogin
from db.database import client_collections
from utils.hash_pass import hash_password, verify_password
from utils.jwt_handler import create_access_token
import secrets

router = APIRouter()

# ✅ Get next auto-increment client id
async def get_next_client_id():
    last_client = await client_collections.find_one(sort=[("id", -1)])
    return last_client["id"] + 1 if last_client else 1

# ✅ Register route
@router.post("/register")
async def register(user: ClientSignup):
    # Check duplicate email
    if await client_collections.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check duplicate username
    if await client_collections.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["id"] = await get_next_client_id()
    user_dict["api_key"] = secrets.token_hex(16)  # Secure api_key generation

    result = await client_collections.insert_one(user_dict)

    return {
        "message": "User registered successfully",
        "id": str(result.inserted_id)
    }

# ✅ Login route using ClientLogin model for cleaner request validation
@router.post("/login")
async def login(user: ClientLogin):
    user_in_db = await client_collections.find_one({"email": user.email})

    if not user_in_db:
        raise HTTPException(status_code=404, detail="Email not registered")

    if not verify_password(user.password, user_in_db["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "id": user_in_db["id"],
        "username": user_in_db["username"],
        "email": user_in_db["email"],
    })

    return {
        "access_token": token,
        "token_type": "bearer",
    }

