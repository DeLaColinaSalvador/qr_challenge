import qrcode
import qrcode.constants
from qrcode.image.pil import PilImage
from io import BytesIO
from sqlalchemy.orm import Session
from app.db.models import QRCode
from fastapi import HTTPException

def generate_qr_image(data: str, color: str, size: int) -> BytesIO:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
    
    img: PilImage = qr.make_image(fill_color=color, back_color="white")
    buffer = BytesIO()
    img = img.resize((int(size), int(size)))
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def create_qr_code(db: Session, user_uuid: str, data: dict) -> BytesIO:
    buffer = generate_qr_image(data["url"], data["color"], data["size"])
    
    new_qr_code = QRCode(
        url=data["url"],
        color=data["color"],
        size=data["size"],
        user_uuid=user_uuid
    )
    db.add(new_qr_code)
    db.commit()
    db.refresh(new_qr_code)
    return buffer

def update_qr_code(db: Session, qr_uuid: int, data: dict) -> BytesIO:
    qr_code = db.query(QRCode).filter(QRCode.uuid == qr_uuid).first()
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR Code not found")
    
    qr_code.url = data["url"]
    qr_code.color = data["color"]
    qr_code.size = data["size"]
    db.commit()
    
    return generate_qr_image(data["url"], data["color"], data["size"])

def fetch_qr_codes_by_user(db: Session, user_uuid: str):
    return db.query(QRCode).filter(QRCode.user_uuid == user_uuid).all()

