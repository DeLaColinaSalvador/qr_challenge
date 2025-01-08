from fastapi import APIRouter
from app.src.routes.user_routes import router as user_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["Users"])