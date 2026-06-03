from datetime import datetime, date
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TIMESTAMP

from betr_eats.db.conn import Connection

Base = declarative_base()

class Goals(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    goal_date = Column(Date)
    goal_value = Column(Float)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __init__(
        self, goal_date: date, goal_value: float
    ):
        self.goal_date = goal_date
        self.goal_value = goal_value
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"<Goals {self.goal_date} ({self.goal_value} lbs)>"

    def insert(self, conn: Connection):
        conn.session.add(self)
        conn.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "goal_date": self.goal_date,
            "goal_value": self.goal_value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def update_goal(cls, conn: Connection, goal_id: int, goal_value: float, goal_date: str):
        conn.session.query(Goals).filter(Goals.id == goal_id).update({
            Goals.goal_value: goal_value,
            Goals.goal_date: goal_date,
            Goals.updated_at: datetime.now(),
        })
        conn.session.commit()
        return "success"
        
    @classmethod
    def delete_goal(self, conn: Connection, goal_id: int):
        conn.session.query(Goals).filter(Goals.id == goal_id).delete()
        conn.session.commit()
        return "success"

    @classmethod
    def get_goal_by_id(cls, conn: Connection, goal_id: int):
        return conn.session.query(cls).filter(cls.id == goal_id).first()

    @classmethod
    def get_goal_by_date(cls, conn: Connection, goal_date: str):
        return conn.session.query(cls).filter(cls.goal_date == goal_date).all()
        