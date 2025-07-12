from fastapi import FastAPI, APIRouter, Request, Response
from routes import auth, show, user
from config import ALLOWED_ORIGINS
from fastapi.routing import APIRoute

from fastapi.middleware.cors import CORSMiddleware

class PreflightRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request):
            if request.method == "OPTIONS":
                return Response(status_code=200)
            return await original_route_handler(request)
        return custom_route_handler
    
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {"message": "Welcome to LockAPI backend"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(show.router, tags=["Client"])
app.include_router(user.router, tags=["user"])
