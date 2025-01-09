import jwt
import datetime
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db.models import User
from dotenv import dotenv_values

config = dotenv_values(".env")

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = "HS256"

http_bearer = HTTPBearer()

def create_access_token(data: dict):
    """Generate JWT token"""
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def register_user(db: Session, email: str, password: str):
    """Register a new user and return JWT token"""
    user = User(email=email)
    user.set_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(data={"sub": user.email, "uuid": user.uuid})
    return user, token

def authenticate_user(db: Session, email: str, password: str):
    """Authenticate user and return JWT token"""
    user = db.query(User).filter(User.email == email).first()
    if user and user.verify_password(password):
        token = create_access_token(data={"sub": user.email, "uuid": user.uuid})
        return token
    return None


def get_user_from_jwt(authorization: str = Depends(http_bearer)):
    try:
        token = authorization.credentials  # JWT token is directly in authorization.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload["uuid"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")