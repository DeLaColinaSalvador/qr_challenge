import pytest
from fastapi.testclient import TestClient
from app.db.database import sessionmaker , create_engine , Base , get_db_session
from app.src.main import app  # Adjust the import path as necessary
from app.db.models import User  # Import your User model
from app.db.schemas import UserCreateSchema  # Import the schema for the user registration

### TESTING STILL NOT IMPLEMENTED

# Define an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create an engine for the test database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture to provide a database session for each test.
    """
    with SessionLocal() as session:
        Base.metadata.create_all(bind=engine)  # Ensure the schema is created before tests run
        yield session
        session.rollback()  # Rollback any changes after the test


@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture to provide a TestClient for the FastAPI app with the in-memory database.
    """
    # Override the `get_db_session` dependency to use the in-memory database session
    def get_session_override():
        return db_session

    app.dependency_overrides[get_db_session] = get_session_override

    # Create the TestClient instance for testing
    client = TestClient(app)
    yield client

@pytest.fixture
def test_user():
    """
    Fixture to provide test user data.
    """
    return UserCreateSchema(email="test@example.com", password="testpassword")


def test_register_user(client, db_session, test_user):
    """
    Test case for registering a new user.
    """

    # Step 1: Ensure no user already exists with the given email
    existing_user = db_session.query(User).filter(User.email == test_user.email).first()
    assert existing_user is None

    # Broken dependency injection, currently using "main" db instead of sqlite in-memory
    # Step 2: Make a POST request to register the user
    response = client.post("/users/register", json={"email": test_user.email, "password": test_user.password})

    data = response.json()
    
    print(data)
    
    # Step 3: Assert that the user is successfully registered and the response is correct
    assert response.status_code == 200
    

    # Assert the expected response data for the newly created user
    assert data["email"] == test_user.email
    assert "uuid" in data  # Ensure that a UUID is returned
    assert "created_at" in data  # Ensure that a creation date is returned
    assert "qr_codes" in data  # Ensure that the list of QR codes is included


# def test_register_user_already_exists(client, db_session, test_user):
#     """
#     Test case for attempting to register a user that already exists.
#     """

#     # Step 1: Create a user manually in the database before testing
#     new_user = User(email=test_user.email, password=test_user.password)
#     db_session.add(new_user)
#     db_session.commit()

#     # Step 2: Try to register the same user again
#     response = client.post("/users/register", json={"email": test_user.email, "password": test_user.password})

#     # Step 3: Assert that the response indicates the email is already registered
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Email is already registered."}
