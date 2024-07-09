import random

from src.generators.equipment_generator import generate_initial_inventory
from src.emulation.workshop_decision_maker import WorkshopDecisionMaker
from src.models.inventory import Inventory
from src.models.service import Service
from src.models.transaction import Transaction, TransactionMethod, TransactionTypes
from src.models.workshop import Workshop


class WorkshopEmulator:
    def __init__(
        self,
        date,
        decision_maker: WorkshopDecisionMaker,
        service_parameters,
        margin,
        equipment,
        personal_data_generator,
    ):
        self.decision_maker = decision_maker
        self.workshop = Workshop(date, personal_data_generator)
        self.manager = decision_maker.create_manager(self.workshop, date)
        self.mechanics = [
            self.decision_maker.create_mechanic(self.workshop, date)
            for _ in range(self.workshop.stations_number)
        ]
        self.margin = margin
        self.repairs = []
        self.active_repairs = []
        self.vehicles = []
        self.vehicles_available_for_sale = []
        self.service_parameters = service_parameters
        self.current_employees = [self.manager] + self.mechanics
        self.employees = [self.manager] + self.mechanics
        self.equipment = equipment
        self.inventory = generate_initial_inventory(
            date=date,
            equipment=self.equipment,
            workshop=self.workshop,
            n=self.decision_maker.initial_equipment_number,
        )
        self.inventory_in_stock = self.inventory

    def add_service_and_create_transaction(self, date, customer):
        order_type = self.decision_maker.choose_order_type(
            self.vehicles_available_for_sale
        )
        if order_type == "repair":
            return self.create_repair_service(date, customer)
        elif order_type == "buy":
            return self.sell_vehicle(date, customer)
        else:
            return self.buy_vehicle(date, customer)

    def create_repair_service(self, date, customer):
        vehicle = self.decision_maker.generate_vehicle(self.workshop)
        self.vehicles.append(vehicle)
        service = Service(
            date=date,
            employee=random.choice(self.mechanics),
            vehicle=vehicle,
            service_parameters=self.service_parameters,
        )
        repair_cost = (service.work_cost + service.part_cost) * (1 + self.margin)
        transaction = Transaction(
            transaction_method=random.choices(
                list(TransactionMethod), weights=[0.2, 0.8]
            )[0],
            sender=customer,
            date=date,
            transaction_type=TransactionTypes["income"],
            value=repair_cost,
        )
        vehicle.price += repair_cost
        service.transaction = transaction
        self.active_repairs.append(service)
        self.repairs.append(service)
        return transaction

    def sell_vehicle(self, date, customer):
        vehicle = random.choice(self.vehicles_available_for_sale)
        self.vehicles_available_for_sale.remove(vehicle)
        transaction = Transaction(
            transaction_method=TransactionMethod["card"],
            sender=customer,
            date=date,
            transaction_type=TransactionTypes["income"],
            value=vehicle.price * random.uniform(1.1, 1.3),
        )
        vehicle.sale = transaction
        return transaction

    def buy_vehicle(self, date, customer):
        vehicle = self.decision_maker.generate_vehicle(self.workshop)
        self.vehicles.append(vehicle)
        transaction = Transaction(
            transaction_method=TransactionMethod["card"],
            sender=customer,
            date=date,
            transaction_type=TransactionTypes["cost"],
            value=vehicle.price,
        )
        vehicle.purchase = transaction
        service = Service(
            date=date,
            employee=random.choice(self.mechanics),
            vehicle=vehicle,
            service_parameters=self.service_parameters,
        )
        self.active_repairs.append(service)
        self.repairs.append(service)
        return transaction

    def complete_repairs(self, date):
        repairs_to_complete = self.decision_maker.choose_repairs_to_complete(
            self.active_repairs
        )
        for repair in repairs_to_complete:
            equipment_to_use = next(
                filter(lambda obj: obj.part == repair.part, self.inventory_in_stock),
                None,
            )
            if equipment_to_use:
                repair.end_date = date
                self.inventory_in_stock.remove(equipment_to_use)
                equipment_to_use.service = repair
                self.active_repairs.remove(repair)
            if repair.vehicle.purchase:
                self.vehicles_available_for_sale.append(repair.vehicle)

    def employee_turnover(self, date):
        for employee in self.current_employees:
            if random.random() < self.decision_maker.employee_resignation_probability:
                employee.resignation_date = date
                if employee.position == "MENADŻER":
                    new_employee = self.decision_maker.create_manager(
                        self.workshop, date
                    )
                else:
                    new_employee = self.decision_maker.create_mechanic(
                        self.workshop, date
                    )
                self.employees.append(new_employee)
                self.current_employees.append(new_employee)
                self.current_employees.remove(employee)

    def stock_replenishment(self, date):
        for equipment in self.equipment:
            equipment_number_in_stock = len(
                list(
                    filter(
                        lambda obj: obj.equipment == equipment, self.inventory_in_stock
                    )
                )
            )
            if (
                equipment_number_in_stock
                < self.decision_maker.number_of_items_in_stock
                / self.decision_maker.stock_replenishment_fraction
            ):
                number_to_buy = (
                    self.decision_maker.number_of_items_in_stock
                    - equipment_number_in_stock
                )
                new_inventory = [
                    Inventory(
                        delivery_date=date,
                        equipment=equipment,
                        workshop=self.workshop,
                        part_name=equipment.name,
                    )
                    for _ in range(number_to_buy)
                ]
                self.inventory_in_stock += new_inventory
                self.inventory += new_inventory
