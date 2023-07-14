from fastapi import APIRouter

from .api.routers import router as api_routers
from .auth.routers import router as auth_routers

routers = APIRouter()
doc_router = APIRouter()

routers.include_router(auth_routers, prefix="/auth", tags=["authentication"])

routers.include_router(api_routers, prefix="/salary", tags=["salary"])
