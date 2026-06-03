from datetime import datetime, date
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TIMESTAMP

from betr_eats.db.conn import Connection

Base = declarative_base()


class Weight(Base):
    __tablename__ = "weight"
    id = Column(Integer, primary_key=True)
    weight_date = Column(Date)
    weight_lbs = Column(Float)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __init__(self, weight_date: date, weight_lbs: float):
        self.weight_date = weight_date
        self.weight_lbs = weight_lbs
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"<Weight {self.weight_date} ({self.weight_lbs} lbs)>"

    def _date_exists(self, conn: Connection):
        return conn.session.query(Weight).filter(Weight.weight_date == self.weight_date).first() is not None

    def insert(self, conn: Connection):
        if self._date_exists(conn):
            return f"Weight for date {self.weight_date} already exists"
        conn.session.add(self)
        conn.session.commit()
        return "success"

    def to_dict(self):
        return {
            "id": self.id,
            "weight_date": self.weight_date,
            "weight_lbs": self.weight_lbs,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def update_weight(cls, conn: Connection, weight_id: int, weight_lbs: float, weight_date: str):
        conn.session.query(Weight).filter(Weight.id == weight_id).update({
            Weight.weight_lbs: weight_lbs,
            Weight.weight_date: weight_date,
            Weight.updated_at: datetime.now(),
        })
        conn.session.commit()
        return "success"

    @classmethod
    def delete_weight(self, conn: Connection, weight_id: int):
        conn.session.query(Weight).filter(Weight.id == weight_id).delete()
        conn.session.commit()
        return "success"

    @classmethod
    def get_weight_by_id(cls, conn: Connection, weight_id: int):
        return conn.session.query(cls).filter(cls.id == weight_id).first()

    @classmethod
    def get_weight_by_date(cls, conn: Connection, weight_date: str):
        return conn.session.query(cls).filter(cls.weight_date == weight_date).all()