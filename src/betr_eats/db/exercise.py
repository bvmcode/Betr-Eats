from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TIMESTAMP

from betr_eats.db.conn import Connection

Base = declarative_base()

class Exercise(Base):
    __tablename__ = "exercise"
    id = Column(Integer, primary_key=True)
    exercise_date = Column(Date)
    excercise_minutes = Column(Integer)
    exercise_description = Column(String)
    exercise_calories_burned = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __init__(self, exercise_date: date, excercise_minutes: int, exercise_description: str, exercise_calories_burned: int):
        self.exercise_date = exercise_date
        self.excercise_minutes = excercise_minutes
        self.exercise_description = exercise_description
        self.exercise_calories_burned = exercise_calories_burned
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"<Exercise on {self.exercise_date}: {self.exercise_description} ({self.exercise_calories_burned} calories)>"

    def insert(self, conn: Connection):
        conn.session.add(self)
        conn.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "exercise_date": self.exercise_date,
            "excercise_minutes": self.excercise_minutes,
            "exercise_description": self.exercise_description,
            "exercise_calories_burned": self.exercise_calories_burned,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def update_exercise(cls, conn: Connection, exercise_id: int, excercise_minutes: int, exercise_description: str, exercise_calories_burned: int, exercise_date: str):
        conn.session.query(Exercise).filter(Exercise.id == exercise_id).update({
            Exercise.excercise_minutes: excercise_minutes,
            Exercise.exercise_description: exercise_description,
            Exercise.exercise_calories_burned: exercise_calories_burned,
            Exercise.exercise_date: exercise_date,
            Exercise.updated_at: datetime.now(),
        })
        conn.session.commit()
        return "success"

    @classmethod
    def delete_exercise(self, conn: Connection, exercise_id: int):
        conn.session.query(Exercise).filter(Exercise.id == exercise_id).delete()
        conn.session.commit()
        return "success"

    @classmethod
    def get_exercise_by_id(cls, conn: Connection, exercise_id: int):
        return conn.session.query(cls).filter(cls.id == exercise_id).first()

    @classmethod
    def get_exercise_by_date(cls, conn: Connection, exercise_date: str):
        return conn.session.query(cls).filter(cls.exercise_date == exercise_date).all()
        