from sqlalchemy import create_engine, inspect, text , Column, Integer, String, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.url import URL
import datetime
import logging
import psycopg2

connection = psycopg2.connect(
    dbname="testqr",
    user="postgresql",
    password="postgresqlpassword",
    host="localhost",
    options="-c client_encoding=UTF8"
)

with connection.cursor() as cursor:
    cursor.execute("SHOW client_encoding;")
    print(f"Client encoding: {cursor.fetchone()[0]}")
connection.close()

# Set up logging to see what's happening
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    uuid = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    # Adding explicit collation for string fields
    email = Column(String(50), nullable=False)
    password_hash = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

def test_database_connection():
    """
    Test each step of database initialization to identify where things break down.
    """
    try:
        # Step 1: Test basic connection
        print("Step 1: Testing database connection...")
        DATABASE_URL = 'postgresql+psycopg2://postgresql:postgresqlpassword@localhost/testqr'
        
        connection_args = {
            'drivername': 'postgresql+psycopg2',
            'username': 'postgresql',
            'password': 'postgresqlpassword',
            'host': 'localhost',
            'database': 'testqr',
        }
        
        #Create the engine with specific PostgreSQL connection parameters
        engine = create_engine(
            URL.create(**connection_args),
            connect_args={
                "client_encoding": "utf8",
                "options": "-c client_encoding=UTF8"
            },
            echo=True
        )
        
        #engine = create_engine("sqlite:///testqr.db")
        
        # Step 2: Test if we can connect
        print("\nStep 2: Testing if database exists and is accessible...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Basic connection successful!")
            
        # Step 3: Check if Base has the models registered
        print("\nStep 3: Checking registered models...")
        for table in Base.metadata.tables.keys():
            print(f"Found model: {table}")
            
        # Step 4: Try to create tables
        print("\nStep 4: Attempting to create tables...")
        Base.metadata.create_all(bind=engine)
        
        # Step 5: Verify tables were created
        print("\nStep 5: Verifying created tables...")
        inspector = inspect(engine)
        for table_name in inspector.get_table_names():
            print(f"Table exists: {table_name}")
            for column in inspector.get_columns(table_name):
                print(f"  Column: {column['name']} ({column['type']})")
                
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    test_database_connection()