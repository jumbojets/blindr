from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config


def create_db_url():
    # Load database configuration from the .env file
    db_config = {
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD'),
        'host': config('DB_HOST'),
        'port': config('DB_PORT'),
        'database': config('DB_NAME')
    }

    # Construct the database URL
    db_url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    return db_url

Base = declarative_base()

class PermanentStorage(Base):
    __tablename__ = 'permanent_storage'
    id = Column(Integer, primary_key=True)
    constraints_hash = Column(String, unique=True, nullable=False)
    private_key = Column(String, nullable=False)
    public_key = Column(String, nullable=False)
    file_hash = Column(String, nullable=True)

class TemporaryStorage(Base):
    __tablename__ = 'temporary_storage'
    id = Column(Integer, primary_key=True)
    constraints_hash = Column(String, unique=True, nullable=False)
    private_value = Column(String, nullable=False)
    public_value = Column(String, nullable=False)
    file_hash = Column(String, nullable=True)


engine = create_engine(create_db_url(), echo=True)
# Create the tables
Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)

# # Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
