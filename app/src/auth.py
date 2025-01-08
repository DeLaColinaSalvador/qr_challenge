import jwt
import datetime
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.models import User
from dotenv import dotenv_values

config = dotenv_values(".env")

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
