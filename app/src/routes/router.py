from fastapi import APIRouter
from app.src.routes.user_routes import router as user_router
from app.src.routes.qr_codes_routes import router as qr_router
from app.src.routes.scan_routes import router as scan_router
from app.src.routes.stat_routes import router as stat_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(qr_router, prefix="/qrcodes", tags=["QRCodes"])
router.include_router(scan_router, prefix="/scan", tags=["Scan"])
router.include_router(stat_router, prefix="/stat", tags=["Stat"])