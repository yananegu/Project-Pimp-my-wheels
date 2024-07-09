import sqlalchemy as sa
from sqlalchemy.orm import relationship
from unidecode import unidecode
from sqlalchemy.dialects.mysql import INTEGER

from src.models.base import Base


class Customer(Base):
    __tablename__ = "customers"
    id = sa.Column(
        "id",
        INTEGER(unsigned=True),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    name = sa.Column("name", sa.String(50), nullable=False)
    surname = sa.Column("surname", sa.String(50), nullable=False)
    email = sa.Column("email", sa.String(60), nullable=False)
    phone_number = sa.Column("phone_number", sa.String(12), nullable=False)
    birth_date = sa.Column("birth_date", sa.Date, nullable=False)
    address = sa.Column("address", sa.String(200), nullable=False)
    account_creation_date = sa.Column("account_creation_date", sa.Date, nullable=False)
    account_deletion_date = sa.Column("account_deletion_date", sa.Date)
    last_active = sa.Column("last_active", sa.Date)

    transactions = sa.orm.relationship("Transaction", back_populates="sender")

    def __init__(self, date, personal_data_generator):
        self.name, self.surname = personal_data_generator.get_unique_name_surname()
        self.email = f"{unidecode(self.name)}.{unidecode(self.surname)}@customer.com"
        self.phone_number = personal_data_generator.get_phone_number()
        self.address = personal_data_generator.get_address(customer=True)
        self.birth_date = personal_data_generator.get_birth_date(date)
        self.account_creation_date = date
        self.account_deletion_date = None
        self.last_active = date
