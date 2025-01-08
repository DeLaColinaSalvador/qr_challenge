import jwt
import datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.models import User
from dotenv import dotenv_values

config = dotenv_values(".env")

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

def get_user_from_jwt(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        # Decode the JWT to get the user info (e.g., user UUID)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_uuid = payload.get("sub")  # Assuming 'sub' is used for user UUID
        if user_uuid is None:
            raise HTTPException(status_code=403, detail="User not found in token")
        return user_uuid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid JWT token")