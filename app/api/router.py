from fastapi import APIRouter

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.vr import router as vr_router

api_router = APIRouter()
api_router.include_router(vr_router, 
                          prefix="/vr", 
                          tags=["vr"])
api_router.include_router(dashboard_router, 
                          prefix="/dashboard", 
                          tags=["dashboard"])
