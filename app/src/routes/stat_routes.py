from fastapi import APIRouter, HTTPException, Depends, status , Response
from typing import Optional
from sqlalchemy.orm import Session
from app.db.database import get_db_session
from app.src.auth import get_user_from_jwt
from app.src.services.stat_service import get_total_scans , get_scan_logs

router = APIRouter()

@router.get("/total/{qr_uuid}")
def total_scans(
        qr_uuid: int,
        db: Session = Depends(get_db_session),
        user_uuid: int = Depends(get_user_from_jwt)
    ):
    """
    Retrieve the total number of scans for a specific QR code.
    """
    try:
        total = get_total_scans(db, qr_uuid, user_uuid)
        return {"qr_uuid": qr_uuid, "total_scans": total}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/details/{qr_uuid}")
def scan_logs(
        qr_uuid: int,
        db: Session = Depends(get_db_session),
        user_uuid: int = Depends(get_user_from_jwt),
        limit: Optional[int] = 10,
        offset: Optional[int] = 0
    ):
    """
    Retrieve detailed scan logs for a specific QR code (IP, country, timestamp).
    
    - **limit**: Maximum number of scan logs to return (default: 10).
    - **offset**: Number of scan logs to skip before starting to return results (default: 0).
    """
    try:
        logs, total = get_scan_logs(db, qr_uuid, user_uuid, limit, offset)
        return {
            "qr_uuid": qr_uuid,
            "total_logs": total,
            "limit": limit,
            "offset": offset,
            "scan_logs": logs,
        }
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)