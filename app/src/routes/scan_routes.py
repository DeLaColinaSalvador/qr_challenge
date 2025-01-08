from fastapi import APIRouter, HTTPException, Depends, status , Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db_session
from app.src.auth import get_user_from_jwt
from app.src.services.scan_service import record_scan

router = APIRouter()

@router.get("/{qr_uuid}")
async def scan_qr_code(
    qr_uuid: int,
    db: Session = Depends(get_db_session),
    request: Request = Request
):
    """
    Simulate a QR code scan, recording client information like IP, country, and timestamp.
    Returns an HTTP 302 redirect to the associated URL of the QR code.
    """
    client_ip = request.client.host
    
    print(client_ip)
    
    try:
        redirect_url = record_scan(db, qr_uuid, client_ip)
        
        # Create a RedirectResponse
        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"  # Adjust this to specific origins if needed
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"  # Allow methods that your frontend might use
        response.headers["Access-Control-Allow-Headers"] = "*"  # Or specify the necessary headers
        return response
    except HTTPException as e:
        raise e