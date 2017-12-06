from ..extensions import db
from .models import Transaction, ADD, SUB


def create_add_transaction_from_order(order, stock):
    db.session.add(order)
    for order_item in order:
        user = order.user
        product = order_item.item.product
        lot_number = order_item.lot_number
        total_units = order_item.amount * order_item.item.units
        expiration_date = order_item.expiration_date
        transaction = Transaction(
            user,
            product,
            lot_number,
            total_units,
            stock,
            ADD,
            expiration_date,
        )
        db.session.add(transaction)
    db.session.commit()

def create_sub_transaction(user, product, lot_number, amount, stock):
    try:
        transaction = Transaction(
            user,
            product,
            lot_number,
            amount,
            stock,
            SUB,
        )
        db.session.add(transaction)
        db.session.commit()
    except ValueError as error:
        print(error)
