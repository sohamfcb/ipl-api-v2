# from fastapi import FastAPI, APIRouter
# from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker, declarative_base
import sqlalchemy as db
from sqlalchemy import create_engine
from datetime import date

from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

from pydantic_models import StudentSchema

load_dotenv()

password=quote_plus(os.getenv("DB_PASSWORD"))
database_uri=f"postgresql://postgres:{password}@localhost:5432/postgres"

engine=create_engine(database_uri)

SessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base=declarative_base()

class User(Base):

    __tablename__="ipl_users"

    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    username=db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)
    email=db.Column(db.String, unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email
        }
    
def connect_to_server():
    database_uri=f"postgresql://postgres:{password}@localhost:5432/postgres"

    engine=create_engine(database_uri)

    SessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine)
    Base=declarative_base()

    return engine, SessionLocal, Base