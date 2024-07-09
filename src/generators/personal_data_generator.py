import random
from datetime import timedelta

import mimesis
import scipy
from scipy.stats import norm
from unidecode import unidecode


class PersonalDataGenerator:
    def __init__(
        self,
        names,
        female_surnames,
        male_surnames,
        min_age=18,
        avg_age=30,
        max_age=80,
        age_scale=15,
    ):
        self.names = names
        self.female_surnames = female_surnames
        self.male_surnames = male_surnames
        self.min_age = min_age
        self.avg_age = avg_age
        self.max_age = max_age
        self.age_scale = age_scale
        self.phone_numbers = set()
        self.addresses = set()
        self.name_surname_pairs = set()
        self.city = mimesis.Address(locale=mimesis.Locale.PL).city()

    def get_unique_name_surname(self):
        def get_name_surname():
            _, name, sex, _ = self.names.sample(n=1, weights="frequency").iloc[0]
            if sex == "F":
                surname = self.female_surnames.sample(
                    n=1, weights="frequency"
                ).surname.iloc[0]
            else:
                surname = self.male_surnames.sample(
                    n=1, weights="frequency"
                ).surname.iloc[0]
            return name, surname

        unique_name, unique_surname = get_name_surname()
        while (
            f"{unidecode(unique_name)}{unidecode(unique_surname)}"
            in self.name_surname_pairs
        ):
            unique_name, unique_surname = get_name_surname()
        self.name_surname_pairs.add(
            f"{unidecode(unique_name)}{unidecode(unique_surname)}"
        )
        return unique_name, unique_surname

    def get_phone_number(self):
        phone_number = str(random.randint(100000000, 999999999))
        while phone_number in self.phone_numbers:
            phone_number = str(random.randint(100000000, 999999999))
        self.phone_numbers.add(phone_number)
        return phone_number

    def get_address(self, customer=False):
        if customer:
            city = random.choices(
                [self.city, mimesis.Address(locale=mimesis.Locale.PL).city()],
                weights=[0.8, 0.2],
            )[0]
        else:
            city = self.city
        address = mimesis.Address(locale=mimesis.Locale.PL).address()
        while address in self.addresses:
            address = mimesis.Address(locale=mimesis.Locale.PL).address()
        self.addresses.add(address)
        return f"{address}, {city}"

    def get_birth_date(self, day):
        a, b = (self.min_age - self.avg_age) / self.age_scale, (
            self.max_age - self.avg_age
        ) / self.age_scale
        age = scipy.stats.truncnorm.rvs(
            a=a, b=b, loc=self.avg_age, scale=self.age_scale
        )
        return day - timedelta(days=age * 365)
