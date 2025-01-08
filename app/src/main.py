from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
from app.src.routes.router import router
from app.db.database import get_db_session
from app.db.models import User
from sqlalchemy.orm import Session

app = FastAPI()

config = dotenv_values(".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)      

app.include_router(router)

@app.get("/test")
async def read_users(db: Session = Depends(get_db_session)):
    users = db.query(User).all()
    return users
