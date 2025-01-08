from sqlalchemy.orm import Session
from app.db.models import QRCode, Scan
from fastapi import HTTPException
import geoip2.database

def record_scan(db: Session, qr_uuid: int, client_ip: str):
    
    # Get the QR code from the database
    qr_code = db.query(QRCode).filter(QRCode.uuid == qr_uuid).first()
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR code not found")
    
    try:
        data = get_country_and_timezone_from_ip(client_ip)
        country = data["country"]
        timezone = data["timezone"]
    except Exception:
        country = "Unknown"
        timezone = "Unknown"

    # Record the scan log in the database
    new_scan_log = Scan(
        qr_uuid = qr_uuid,
        ip = client_ip,
        country = country,
        timezone = timezone
    )
    db.add(new_scan_log)
    db.commit()

    return qr_code.url  # Return the URL for the redirect


def get_country_and_timezone_from_ip(ip: str) -> dict:
    try:
        with geoip2.database.Reader('/path/to/GeoLite2-City.mmdb') as reader:
            # Use the 'city' method to retrieve detailed location information
            response = reader.city(ip)
            
            country = response.country.name
            timezone = response.location.time_zone if response.location.time_zone else "Unknown"
            
            return {"country": country, "timezone": timezone}
    except Exception:
        return {"country": "Unknown", "timezone": "Unknown"}


