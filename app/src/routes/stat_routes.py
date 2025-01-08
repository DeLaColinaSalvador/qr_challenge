from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db_session
from app.src.auth import get_user_from_jwt
from app.src.services.stat_service import get_total_scans , get_scan_logs

router = APIRouter()

@router.get("/total/{qr_uuid}")
def total_scans(
        qr_uuid: int,
        db: Session = Depends(get_db_session),
        user_uuid : int = Depends(get_user_from_jwt)
    ):
    """
    Retrieve the total number of scans for a specific QR code.
    """
    total = get_total_scans(db, qr_uuid)
    return {"qr_uuid": qr_uuid, "total_scans": total}


@router.get("/details/{qr_uuid}")
def scan_logs(
        qr_uuid: int,
        db: Session = Depends(get_db_session),
        user_uuid : int = Depends(get_user_from_jwt)
    ):
    """
    Retrieve detailed scan logs for a specific QR code (IP, country, timestamp).
    """
    logs = get_scan_logs(db, qr_uuid)
    return {
        "qr_uuid": qr_uuid,
        "scan_logs": logs,
    }