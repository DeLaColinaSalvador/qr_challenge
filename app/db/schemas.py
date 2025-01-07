from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Base Schemas


class UserBaseSchema(BaseModel):
    email: str


class QRCodeBaseSchema(BaseModel):
    url: str
    color: str
    size: str


class ScanBaseSchema(BaseModel):
    ip: str
    country: str
    timezone: str


# Create Schemas

class UserCreateSchema(UserBaseSchema):
    password_hash: str


class QRCodeCreateSchema(QRCodeBaseSchema):
    user_uuid: int


class ScanCreateSchema(ScanBaseSchema):
    qr_uuid: int


# Response Schemas


class ScanResponseSchema(ScanBaseSchema):
    uuid: int
    qr_uuid: int

    class Config:
        from_attributes = True


class QRCodeResponseSchema(QRCodeBaseSchema):
    uuid: int
    user_uuid: int
    created_at: datetime
    updated_at: datetime
    scans: List[ScanResponseSchema] = []

    class Config:
        from_attributes = True


class UserResponse(UserBaseSchema):
    uuid: int
    created_at: datetime
    qr_codes: List[QRCodeResponseSchema] = []

    class Config:
        from_attributes = True
