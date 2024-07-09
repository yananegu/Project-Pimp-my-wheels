import scipy
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from unidecode import unidecode
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.dialects.mysql import DECIMAL

from src.models.base import Base


class Employee(Base):
    __tablename__ = "employees"
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
    workshop_id = sa.orm.mapped_column(sa.ForeignKey("workshops.id"), nullable=False)
    position = sa.Column("position", sa.String(100), nullable=False)
    hire_date = sa.Column("hire_date", sa.Date, nullable=False)
    resignation_date = sa.Column("resignation_date", sa.Date)
    salary = sa.Column(
        "salary", DECIMAL(precision=8, scale=2, unsigned=True), nullable=False
    )

    workshop = relationship("Workshop", back_populates="employees")
    repairs = relationship("Service", back_populates="employee")

    def __init__(
        self,
        date,
        workshop,
        personal_data_generator,
        position,
        min_salary,
        avg_salary,
        max_salary,
    ):
        self.workshop = workshop
        self.name, self.surname = personal_data_generator.get_unique_name_surname()
        self.email = (
            f"{unidecode(self.name)}.{unidecode(self.surname)}@pimpmywheels.com"
        )
        self.phone_number = personal_data_generator.get_phone_number()
        self.address = personal_data_generator.get_address()
        self.birth_date = personal_data_generator.get_birth_date(date)
        self.position = position
        self.hire_date = date
        self.resignation_date = None
        self.min_salary = min_salary
        self.avg_salary = avg_salary
        self.max_salary = max_salary
        self.salary = self.get_salary()

    def get_salary(self):
        scale = (self.avg_salary - self.min_salary) / 2
        a, b = (self.min_salary - self.avg_salary) / scale, (
            self.max_salary - self.avg_salary
        ) / scale
        salary = scipy.stats.truncnorm.rvs(a=a, b=b, loc=self.avg_salary, scale=scale)
        return round(salary, 0)
