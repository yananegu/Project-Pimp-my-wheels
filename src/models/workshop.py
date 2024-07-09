import random

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER

from src.models.base import Base


class Workshop(Base):
    __tablename__ = "workshops"
    id = sa.Column(
        "id",
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    address = sa.Column("address", sa.String(100), nullable=False)
    phone_number = sa.Column("phone_number", sa.String(12), nullable=False)
    stations_number = sa.Column(
        "number_of_stations", INTEGER(unsigned=True), nullable=False
    )
    opening_date = sa.Column("opening_date", sa.Date, nullable=False)

    employees = sa.orm.relationship("Employee", back_populates="workshop")
    vehicles = sa.orm.relationship("Vehicle", back_populates="workshop")
    inventory = sa.orm.relationship("Inventory", back_populates="workshop")

    def __init__(self, date, personal_date_generator):
        self.address = personal_date_generator.get_address()
        self.phone_number = personal_date_generator.get_phone_number()
        self.stations_number = random.randint(3, 5)
        self.opening_date = date
