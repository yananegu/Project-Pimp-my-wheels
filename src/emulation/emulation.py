import random


def emulate_day(
    date, workshop_decision_makers, customer_decision_maker, transactions, day_number
):
    customer_decision_maker.accounts_deactivation(date)
    for wdm in workshop_decision_makers:
        wdm.employee_turnover(date)
        wdm.complete_repairs(date)
        if day_number % 7 == 0:
            wdm.stock_replenishment(date)
    customers_today = customer_decision_maker.customers_arrival(date)
    for customer in customers_today:
        wdm = random.choice(workshop_decision_makers)
        transactions.append(wdm.add_service_and_create_transaction(date, customer))
