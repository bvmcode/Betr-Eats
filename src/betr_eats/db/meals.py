from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TIMESTAMP

from betr_eats.db.conn import Connection

Base = declarative_base()

class Meals(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True)
    meal_date= Column(Date)
    meal_type = Column(String)
    meal_description = Column(String)
    calorie_count = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __init__(
        self, meal_date: date, meal_type: str, meal_description: str, calorie_count: int
    ):
        self.meal_date = meal_date
        self.meal_type = meal_type
        self.meal_description = meal_description
        self.calorie_count = calorie_count
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.meal_types = ["breakfast", "lunch", "dinner", "snack", "other"]
        if meal_type not in self.meal_types:
            raise ValueError(f"Invalid meal type: {meal_type}. Must be one of {self.meal_types}")

    def __repr__(self):
        return f"<Meal {self.meal_type} on {self.meal_date}: {self.meal_description} ({self.calorie_count} calories)>"

    def insert(self, conn: Connection):
        conn.session.add(self)
        conn.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "meal_date": self.meal_date,
            "meal_type": self.meal_type,
            "meal_description": self.meal_description,
            "calorie_count": self.calorie_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def update_meal(cls, conn: Connection, meal_id: int, calorie_count: int, meal_description: str, meal_type: str, meal_date: str):
        conn.session.query(Meals).filter(Meals.id == meal_id).update({
            Meals.calorie_count: calorie_count,
            Meals.meal_description: meal_description,
            Meals.meal_type: meal_type,
            Meals.meal_date: meal_date,
            Meals.updated_at: datetime.now(),
        })
        conn.session.commit()
        return "success"

    @classmethod
    def delete_meal(self, conn: Connection, meal_id: int):
        conn.session.query(Meals).filter(Meals.id == meal_id).delete()
        conn.session.commit()
        return "success"

    @classmethod
    def get_meal_by_id(cls, conn: Connection, meal_id: int):
        return conn.session.query(cls).filter(cls.id == meal_id).first()

    @classmethod
    def get_meal_by_date(cls, conn: Connection, meal_date: str):
        return conn.session.query(cls).filter(cls.meal_date == meal_date).all()