from fastapi import FastAPI, Request, Response, HTTPException, Depends
from routes import auth, show, user
from config import FRONTEND_URL
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

async def only_allow_frontend(request: Request):
    origin = request.headers.get("origin")
    # allowed_origin = FRONTEND_URL
    allowed_origin = "http://localhost:5173"
    if origin != allowed_origin:
        raise HTTPException(status_code=403, detail="Not allowed from this origin")
    return True

@app.get("/")
async def index():
    return {"message": "Welcome to LockAPI backend"}

app.include_router(auth.router, prefix="/auth", tags=["auth"], dependencies=[Depends(only_allow_frontend)])
app.include_router(show.router, tags=["Client"],  dependencies=[Depends(only_allow_frontend)])
app.include_router(user.router, tags=["user"])
