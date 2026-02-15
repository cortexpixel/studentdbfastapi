import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()


from sqlalchemy import Column, Integer, String, Date

class Student(Base):
	__tablename__ = "students"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	date_of_birth = Column(Date, nullable=False)
	gender = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)

from pydantic import BaseModel
from datetime import date
from fastapi import Depends, HTTPException
from typing import List

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
		orm_mode = True

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.post("/students/", response_model=StudentRead)
def create_student(student: StudentCreate, db=Depends(get_db)):
	db_student = Student(**student.dict())
	db.add(db_student)
	db.commit()
	db.refresh(db_student)
	return db_student

@app.get("/students/", response_model=List[StudentRead])
def read_students(db=Depends(get_db)):
	students = db.query(Student).all()
	return students
