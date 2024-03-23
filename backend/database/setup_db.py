from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db_connection import create_db_url

Base = declarative_base()

class PermanentStorage(Base):
    __tablename__ = 'permanent_storage'
    id = Column(Integer, primary_key=True)
    constraints_hash = Column(String, unique=True, nullable=False)
    private_key = Column(String, nullable=False)
    public_key = Column(String, nullable=False)

class TemporaryStorage(Base):
    __tablename__ = 'temporary_storage'
    id = Column(Integer, primary_key=True)
    constraints_hash = Column(String, unique=True, nullable=False)
    private_value = Column(String, nullable=False)
    public_value = Column(String, nullable=False)


engine = create_engine(create_db_url(), echo=True)
# Create the tables
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
