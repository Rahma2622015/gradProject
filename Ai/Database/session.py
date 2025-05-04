from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.DatabaseTabels.database import Base

DATABASE_URL = "sqlite:///university_information.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
