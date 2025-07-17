from fastapi import APIRouter, HTTPException, Path, Body
from models.user import UserSignup, UserLogin, UserOut
from db.database import client_collections, client_user_collections
from utils.hash_pass import hash_password, verify_password

router = APIRouter()

async def get_client_by_api_key(api_key: str):
    client = await client_collections.find_one({"api_key": api_key})
    if not client:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return client

async def get_next_user_id():
    last_user = await client_user_collections.find_one(sort=[("id", -1)])
    return last_user["id"] + 1 if last_user else 1

# 1️⃣ User Register
@router.post("/{api_key}/user/register")
async def user_register(api_key: str = Path(...), user: UserSignup = Body(...)):
    client = await get_client_by_api_key(api_key)
    
    if await client_user_collections.find_one({"email": user.email, "client_id": client["id"]}):
        raise HTTPException(status_code=400, detail="Email already registered for this client")
    
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["id"] = await get_next_user_id()
    user_dict["client_id"] = client["id"]

    await client_user_collections.insert_one(user_dict)
    
    return {"message": "User registered successfully", "user_eamil": user_dict["email"]}

# 2️⃣ User Login
@router.post("/{api_key}/user/login")
async def user_login(api_key: str = Path(...), user: UserLogin = Body(...)):
    client = await get_client_by_api_key(api_key)
    
    user_in_db = await client_user_collections.find_one({"email": user.email, "client_id": client["id"]})
    if not user_in_db:
        raise HTTPException(status_code=404, detail="Email not registered for this client")
    
    if not verify_password(user.password, user_in_db["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    return {
        "message": "Login successful",
        "username": user_in_db["username"],
        "eamil": user_in_db["email"]
    }

# 3️⃣ Show All Users
@router.get("/{api_key}/user/all")
async def show_all_users(api_key: str = Path(...)):
    client = await get_client_by_api_key(api_key)
    
    users_cursor = client_user_collections.find({"client_id": client["id"]})
    users = []
    async for user in users_cursor:
        users.append({
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        })
    return {"total_users": len(users), "users": users}

# 4️⃣ Delete User by Email
@router.delete("/{api_key}/user/delete/{user_email}")
async def delete_user(
    api_key: str = Path(...),
    user_email: str = Path(...)
):
    client = await get_client_by_api_key(api_key)
    
    result = await client_user_collections.delete_one({
        "email": user_email,
        "client_id": client["id"]
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"User with email {user_email} not found for this client"
        )
    
    return {"message": f"User with email {user_email} deleted successfully"}


# ✅ Single user show route for a client by email
@router.get("/{api_key}/user/{user_email}")
async def show_single_user(api_key: str = Path(...), user_email: str = Path(...)):
    client = await client_collections.find_one({"api_key": api_key})
    if not client:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    user = await client_user_collections.find_one({"email": user_email, "client_id": client["id"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found for this client")
    
    user_data = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }
    
    return user_data

