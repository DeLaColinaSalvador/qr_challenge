from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
import re

# Base Schemas

class UserBaseSchema(BaseModel):
    email: str

    @field_validator("email")
    def validate_email(cls, v):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format.")
        return v

class QRCodeBaseSchema(BaseModel):
    url: str
    color: str
    size: str

    @field_validator("url")
    def validate_url(cls, v):
        if not v.startswith("http"):
            raise ValueError("URL must start with 'http'.")
        return v
    
    @field_validator("color")
    def validate_color(cls, v):
        valid_colors = ["red", "green", "blue", "black"]
        if v not in valid_colors:
            raise ValueError(f"Invalid color. Valid options are: {', '.join(valid_colors)}.")
        return v

    @field_validator("size")
    def validate_size(cls, v):
        if not v.isdigit() or int(v) <= 0:
            raise ValueError("Size must be a positive integer.")
        return v


class ScanBaseSchema(BaseModel):
    ip: str
    country: str
    timezone: str

    @field_validator("ip")
    def validate_ip(cls, v):
        # Simple regex for basic IP validation (IPv4)
        ip_regex = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        if not re.match(ip_regex, v):
            raise ValueError("Invalid IP address format.")
        return v

    @field_validator("timezone")
    def validate_timezone(cls, v):
        # Basic validation for timezone (using a common timezone pattern)
        timezone_regex = r"^[A-Za-z]+\/[A-Za-z_]+$"
        if not re.match(timezone_regex, v):
            raise ValueError("Invalid timezone format.")
        return v


# Create Schemas

class UserCreateSchema(UserBaseSchema):
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter.")
        return v

class QRCodeCreateSchema(QRCodeBaseSchema):
    pass

class ScanCreateSchema(ScanBaseSchema):
    qr_uuid: int

    @field_validator("qr_uuid")
    def validate_qr_uuid(cls, v):
        if v <= 0:
            raise ValueError("QR UUID must be a positive integer.")
        return v


# Response Schemas

class ScanResponseSchema(ScanBaseSchema):
    uuid: int
    qr_uuid: int

    class ConfigDict:
        from_attributes = True


class QRCodeResponseSchema(QRCodeBaseSchema):
    uuid: int
    user_uuid: int
    created_at: datetime
    updated_at: datetime
    scans: List[ScanResponseSchema] = []

    @property
    def total_scans(self):
        return len(self.scans)

    class ConfigDict:
        from_attributes = True


class UserResponse(UserBaseSchema):
    uuid: int
    qr_codes: List[QRCodeResponseSchema] = []

    class ConfigDict:
        from_attributes = True
