from contextlib import asynccontextmanager
from datetime import date
from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base, Session


# -----------------------------
# Database Setup (Safe Pattern)
# -----------------------------

Base = declarative_base()

engine = None
SessionLocal = None


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan handler replaces deprecated @app.on_event("startup")
    Ensures DB connection is created AFTER app loads.
    """

    global engine, SessionLocal

    DATABASE_URL = "postgresql+psycopg2://cortexpixel:Cortexpixel_1990@35.238.8.214:5432/test-studentdb"

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables safely at startup
    Base.metadata.create_all(bind=engine)

    yield

    # Cleanup on shutdown
    engine.dispose()


app = FastAPI(lifespan=lifespan)


# -----------------------------
# Pydantic Schemas
# -----------------------------

class StudentCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: str


class StudentRead(BaseModel):
    id: int
    name: str
    date_of_birth: date
    gender: str

    class Config:
        from_attributes = True  # replaces orm_mode in new Pydantic versions


# -----------------------------
# Dependency
# -----------------------------

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Routes
# -----------------------------

@app.post("/students/", response_model=StudentRead)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students/", response_model=List[StudentRead])
def read_students(db: Session = Depends(get_db)):
    return db.query(Student).all()