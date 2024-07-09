import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from src.models.base import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = sa.Column(
        INTEGER(unsigned=True), autoincrement=True, primary_key=True, nullable=False
    )
    purchase_id = sa.orm.mapped_column(sa.ForeignKey("transactions.id"), nullable=True)
    sale_id = sa.orm.mapped_column(sa.ForeignKey("transactions.id"), nullable=True)
    workshop_id = sa.orm.mapped_column(sa.ForeignKey("workshops.id"), nullable=False)
    brand = sa.Column(sa.String(15), nullable=True, comment="Marka pojazdu")
    model = sa.Column(sa.String(15), nullable=True, comment="Model pojazdu")

    purchase = relationship(
        "Transaction", foreign_keys=[purchase_id], back_populates="purchased_vehicles"
    )
    sale = relationship(
        "Transaction", foreign_keys=[sale_id], back_populates="sold_vehicles"
    )
    workshop = relationship(
        "Workshop", foreign_keys=[workshop_id], back_populates="vehicles"
    )
    repair = relationship("Service", back_populates="vehicle")

    def __init__(self, workshop, brand, model, price):
        self.purchase = None
        self.workshop = workshop
        self.brand = brand
        self.model = model
        self.sale = None
        self.price = price
