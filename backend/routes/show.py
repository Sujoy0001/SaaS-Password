from fastapi import HTTPException, APIRouter
from db.database import client_collections

router = APIRouter()

@router.get("/clients/{id}")
async def get_client(id: int):
    client = await client_collections.find_one({"id": id})
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client_data = {
        "id": client["id"],
        "username": client["username"],
        "email": client["email"],
        "api_key": client["api_key"]
    }
    
    return client_data
