from fastapi import APIRouter, HTTPException
from models.client import ClientSignup, ClientLogin
from db.database import client_user_collections
from utils.hash_pass import hash_password, verify_password
from utils.jwt_handler import create_access_token
import secrets

router = APIRouter()

# ✅ Get next auto-increment client id
async def get_next_user_id():
    last_client = await client_user_collections.find_one(sort=[("id", -1)])
    return last_client["id"] + 1 if last_client else 1

# ✅ Register route
@router.post("/register")
async def register(user: ClientSignup):
    # Check duplicate email
    if await client_user_collections.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check duplicate username
    if await client_user_collections.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["id"] = await get_next_user_id()

    result = await client_user_collections.insert_one(user_dict)

    return {
        "message": "User registered successfully",
        "id": str(result.inserted_id)
    }

# ✅ Login route using ClientLogin model for cleaner request validation
@router.post("/login")
async def login(user: ClientLogin):
    user_in_db = await client_user_collections.find_one({"email": user.email})

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

# ✅ Show all users
@router.get("/all")
async def show_all_users():
    users_cursor = client_user_collections.find()
    users = []
    async for user in users_cursor:
        users.append({
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
        })
        
    return {"total_users": len(users), "users": users}

# ✅ Delete user by ID
@router.delete("/{user_id}")
async def delete_user(user_id: int):
    result = await client_user_collections.delete_one({"id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found or already deleted")
    
    return {"message": f"User with id {user_id} deleted successfully"}
