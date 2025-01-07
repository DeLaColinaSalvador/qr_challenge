from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from dotenv import dotenv_values

config = dotenv_values(".env")

for key, value in config.items():
    print(f"{key}: {value}")

Base = declarative_base()

DATABASE_URL = f'postgresql+psycopg2://{quote_plus(config["DB_USER"])}:{quote_plus(config["DB_PASSWORD"])}@{config["DB_HOST"]}/{config["DB_NAME"]}'
print(f'Database connection string: {DATABASE_URL}')

engine = create_engine("sqlite:///testqr.db")

# Create a sessionmaker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to provide a session for each request
def get_db_session():
    session = SessionLocal()
    Base.metadata.create_all(bind=engine)
    try:
        yield session
    finally:
        session.close()