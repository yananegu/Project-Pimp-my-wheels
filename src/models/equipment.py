import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER

from src.models.base import Base


class Equipment(Base):
    __tablename__ = "equipment"
    id = sa.Column(
        INTEGER(unsigned=True),
        autoincrement=True,
        primary_key=True,
        comment="Id wyposażenia",
    )
    name = sa.Column(sa.String(255), nullable=False, comment="Nazwa")
    type = sa.Column(sa.String(50), nullable=False, comment="Typ")
    cost = sa.Column(sa.DECIMAL(8, 2), nullable=False, comment="Koszt")

    inventories = relationship("Inventory", back_populates="equipment")

    def __init__(self, name, type, cost):
        self.name = name
        self.type = type
        self.cost = cost
