from src.models.equipment import Equipment
from src.models.inventory import Inventory


def generate_equipment_table(service_parameters):
    equipment = []
    for service in service_parameters:
        equipment.append(
            Equipment(name=service["part"], type="część", cost=service["part_cost"])
        )
    return equipment


def generate_initial_inventory(date, equipment, workshop, n):
    initial_inventory = []
    for eq in equipment:
        initial_inventory += [
            Inventory(
                delivery_date=date, equipment=eq, workshop=workshop, part_name=eq.name
            )
            for _ in range(n)
        ]
    return initial_inventory
