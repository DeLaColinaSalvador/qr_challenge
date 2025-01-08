from sqlalchemy.orm import Session
from app.db.models import QRCode, Scan
from fastapi import HTTPException

def get_total_scans(db: Session, qr_uuid: int):
    qr_code = db.query(QRCode).filter(QRCode.uuid == qr_uuid).first()
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR code not found")

    total_scans = db.query(Scan).filter(Scan.qr_uuid == qr_uuid).count()
    return total_scans


def get_scan_logs(db: Session, qr_uuid: int, user_uuid: int):
    # Fetch the QR code and check if it belongs to the user
    qr_code = db.query(QRCode).filter(QRCode.uuid == qr_uuid).first()
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR code not found or user is not authorized")
    
    if qr_code.user_uuid != user_uuid:
        raise HTTPException(status_code=401, detail="User is not authorized")

    scan_logs = db.query(Scan).filter(Scan.qr_uuid == qr_uuid).all()
    return [
        {
            "ip_address": log.ip,
            "country": log.country,
            "timestamp": log.created_at,
            "timezone": log.timezone
        }
        for log in scan_logs
    ]