import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.dialects.mysql import DECIMAL
import enum
from src.models.base import Base


class TransactionMethod(enum.Enum):
    cash = 1
    card = 2


class TransactionTypes(enum.Enum):
    income = 1
    cost = 2


class Transaction(Base):
    __tablename__ = "transactions"
    id = sa.Column(
        "id",
        INTEGER(unsigned=True),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    transaction_method = sa.Column(
        "transaction_method", sa.Enum(TransactionMethod), nullable=False
    )
    other_party = sa.orm.mapped_column(sa.ForeignKey("customers.id"), nullable=False)
    date = sa.Column("data", sa.Date, nullable=False)
    transaction_type = sa.Column(
        "transaction_type", sa.Enum(TransactionTypes), nullable=False
    )
    value = sa.Column(
        "value", DECIMAL(precision=8, scale=2, unsigned=True), nullable=False
    )

    sender = sa.orm.relationship("Customer", back_populates="transactions")
    purchased_vehicles = sa.orm.relationship(
        "Vehicle", foreign_keys="Vehicle.purchase_id", back_populates="purchase"
    )
    sold_vehicles = sa.orm.relationship(
        "Vehicle", foreign_keys="Vehicle.sale_id", back_populates="sale"
    )
    repairs = sa.orm.relationship("Service", back_populates="transaction")

    def __init__(self, transaction_method, sender, date, transaction_type, value):
        self.transaction_method = transaction_method
        self.sender = sender
        self.date = date
        self.transaction_type = transaction_type
        self.value = value
