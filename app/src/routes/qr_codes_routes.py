from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.schemas import QRCodeCreateSchema
from app.db.database import get_db_session
from app.src.auth import get_user_from_jwt
from app.src.services.qr_codes_services import create_qr_code, update_qr_code, fetch_qr_codes_by_user
from app.db.models import QRCode

router = APIRouter()

@router.post("/generate")
def generate_qr_code(
    data: QRCodeCreateSchema,
    db: Session = Depends(get_db_session),
    user_uuid: str = Depends(get_user_from_jwt)
):
    """
    Create a new QR code for the authenticated user.
    
    Returns : Image file of the newly created QR code.
    """
    buffer = create_qr_code(db, user_uuid, data.model_dump())
    return StreamingResponse(buffer, media_type="image/png", headers={
        "Content-Disposition": "attachment; filename=generated_qr_code.png"
    })

@router.put("/{qr_uuid}")
def update_qr_code_route(
    qr_uuid: int,
    data: QRCodeCreateSchema,
    db: Session = Depends(get_db_session),
    user_uuid: str = Depends(get_user_from_jwt)
):
    """
    Update an existing QR code for the authenticated user.
    
    Returns : Image file of the updated QR code.
    
    """
    qr_code = db.query(QRCode).filter(QRCode.uuid == qr_uuid).first()
    if not qr_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"QR Code with UUID {qr_uuid} not found."
        )
        
    if not qr_code.user_uuid == user_uuid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authorized"
        )
    
    buffer = update_qr_code(db, qr_uuid, data.model_dump())
    return StreamingResponse(buffer, media_type="image/png", headers={
        "Content-Disposition": f"attachment; filename=updated_qr_code_{qr_uuid}.png"
    })

@router.get("/list-qr/{uuid}")
async def list_qr_codes(
    db: Session = Depends(get_db_session),
    user_uuid: str = Depends(get_user_from_jwt)
):
    """
    List all QR codes. Filtered by a specific user's UUID obtained from JWT.

    Returns:
        List of QR codes belonging to the user.
    """
    
    qr_codes = fetch_qr_codes_by_user(db, user_uuid)
    return {"qr_codes": qr_codes}
