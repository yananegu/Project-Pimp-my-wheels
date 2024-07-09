import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER

from src.models.base import Base


class Inventory(Base):
    __tablename__ = "inventory"
    id = sa.Column(
        INTEGER(unsigned=True),
        autoincrement=True,
        primary_key=True,
    )
    equipment_id = sa.orm.mapped_column(sa.ForeignKey("equipment.id"), nullable=False)
    service_id = sa.orm.mapped_column(sa.ForeignKey("services.id"), nullable=True)
    workshop_id = sa.orm.mapped_column(sa.ForeignKey("workshops.id"), nullable=False)
    delivery_date = sa.Column("delivery_date", sa.Date, nullable=False)

    equipment = relationship("Equipment", back_populates="inventories")
    service = relationship("Service", back_populates="inventory")
    workshop = relationship("Workshop", back_populates="inventory")

    def __init__(self, delivery_date, equipment, workshop, part_name):
        self.equipment = equipment
        self.service = None
        self.workshop = workshop
        self.delivery_date = delivery_date
        self.part = part_name
