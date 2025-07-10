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
        "routes": client["routes"],
    }
    
    return client_data
