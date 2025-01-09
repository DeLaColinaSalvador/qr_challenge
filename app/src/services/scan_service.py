import requests
from sqlalchemy.orm import Session
from app.db.models import QRCode, Scan
from fastapi import HTTPException

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
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            print(data)
            if data["status"] == "success":
                country = data.get("country", "Unknown")
                timezone = data.get("timezone", "Unknown")
                return {"country": country, "timezone": timezone}
            else:
                print(f"GeoIP lookup failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"GeoIP API request failed with status code {response.status_code}")
    except Exception as e:
        print(f"GeoIP lookup failed: {e}")
    return {"country": "Unknown", "timezone": "Unknown"}