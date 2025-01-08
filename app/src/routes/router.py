from fastapi import APIRouter
from app.src.routes.user_routes import router as user_router
from app.src.routes.qr_codes_routes import router as qr_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(qr_router, prefix="/qrcodes", tags=["QRCodes"])