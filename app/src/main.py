from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
from app.src.routes.router import router
from app.db.database import get_db_session
from app.test.dataset import create_testing_dataset

app = FastAPI()

config = dotenv_values(".env")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)      

app.include_router(router)

@app.get('/test')
def test(db = Depends(get_db_session)):
    create_testing_dataset(db)
    return "hello world"