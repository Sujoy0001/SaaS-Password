from fastapi import HTTPException, APIRouter
from db.database import client_collections

router = APIRouter()

@router.get("/clients/{email}")
async def get_client(email: str):
    client = await client_collections.find_one({"email": email})
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client_data = {
        "id": client["id"],
        "username": client["username"],
        "email": client["email"],
        "routes": client["routes"],
    }
    
    return client_data
