from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship
import datetime
from .database import Base
import bcrypt

class User(Base):
    __tablename__ = 'Users'
    uuid = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    qr_codes = relationship('QRCode', back_populates='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return
    
    def verify_password(self, password:str):
        password_byte_enc = password.encode('utf-8')
        hashed_password_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password_bytes)
    
    def __repr__(self):
        return f"<User(uuid={self.uuid}, email={self.email})>"
    

class QRCode(Base):
    __tablename__ = 'QRCodes'
    uuid = Column(Integer, Sequence('qrcodes_id_seq'), primary_key=True)
    url = Column(String(50), nullable=False, unique=True)
    color = Column(String(50))
    size = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    user_uuid = Column(Integer, ForeignKey("Users.uuid", ondelete="CASCADE"), nullable=False)
    
    user = relationship('User', back_populates='qr_codes')
    scans = relationship('Scan', back_populates='qr_code', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<QRCode(uuid={self.uuid}, url={self.url})>"

class Scan(Base):
    __tablename__ = 'Scans'
    uuid = Column(Integer, Sequence('scans_id_seq'), primary_key=True)
    qr_uuid = Column(Integer, ForeignKey("QRCodes.uuid", ondelete="CASCADE"), nullable=False)
    ip = Column(String(50))
    country = Column(String(50))
    timezone = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    qr_code = relationship('QRCode', back_populates='scans')

    def __repr__(self):
        return f"<Scan(uuid={self.uuid}, country={self.country})>"