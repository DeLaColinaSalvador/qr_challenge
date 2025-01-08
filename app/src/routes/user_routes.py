from fastapi import APIRouter, Depends, HTTPException , status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db_session
from app.db.schemas import UserCreateSchema , UserResponse
from app.db.models import User
from app.src.auth import register_user, authenticate_user

router = APIRouter()


@router.post("/register")
def register(user : UserCreateSchema, db: Session = Depends(get_db_session)):
    
    """
    Register a new user.

    - **email**: The email of the user.
    - **password**: The password of the user.

    Returns the created user's details along with a JWT token.
    """
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )

    try:
        # Proceed with registering the new user
        new_user, token = register_user(db, user.email, user.password)

        user_response = UserResponse(
            email=new_user.email,
            uuid=new_user.uuid,
            created_at=new_user.created_at,
            qr_codes=new_user.qr_codes
        )

        response = {"user": user_response, "token": token}

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration."
        )


@router.post("/login")
def login(user : UserCreateSchema, db: Session = Depends(get_db_session)):
    
    """
    Log in an existing user.

    - **email**: The email of the user.
    - **password**: The password of the user.

    Returns a JWT token if the credentials are valid.
    """
    
    token = authenticate_user(db, user.email, user.password)
    if token:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"token": token})
    raise HTTPException(status_code=401, detail="Invalid credentials")


